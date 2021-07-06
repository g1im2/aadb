import os
import re
import struct
from typing import List, Dict

import aiofiles

from aadb.transport import Client, Signal, Stats

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote1


class Transport(object):

    def __init__(self):
        self.device = None

    def transport(self, cls):
        def wrapper(*args, **kwargs):
            device = cls(*args, **kwargs)
            self.device = device
            return device

        return wrapper

    def shell(self, **options):
        def decorator(f):
            async def wrapper(*args, **kwargs):
                async with Client() as client:
                    await client.call('host:transport:{}'.format(self.device.serial))
                    cmd_args = '' if not args else args[0]
                    await client.call('shell:{}'.format(options['command']))
                    await client.receive_lines(pipeline_func=kwargs['pipeline_func'])
                return await f(*args, **kwargs)

            return wrapper

        return decorator

    def host(self, **options):
        def decorator(f):
            async def wrapper(*args, **kwargs):
                async with Client() as client:
                    await client.call('host:{}'.format(options['command']))
                    if 'no_receive' not in options:
                        kwargs['parsing_result'](await client.receive())
                return await f(*args, **kwargs)

            return wrapper

        return decorator

    def push(self, **options):
        def decorator(f):
            async def wrapper(*args, **kwargs):
                async with Client() as client:
                    await client.call('host:transport:{}'.format(self.device.serial))
                    # send sync signal
                    await client.call('sync:')
                    # send sync file info data
                    arg = '{dest},{mode}'.format(dest=kwargs['dest_path'],
                                                 mode=options['mode'] | Stats.S_IFREG).encode('utf-8')
                    await client.write(Signal.SEND.encode('utf-8') + struct.pack('<I', len(arg)) + arg)
                    # send data now
                    total_size = os.path.getsize(kwargs['src_path'])
                    async with aiofiles.open(kwargs['src_path'], 'rb') as stream:
                        sent_size = 0
                        while True:
                            chunk = await stream.read(65536)
                            if not chunk:
                                break
                            sent_size += len(chunk)
                            await client.write(Signal.DATA.encode('utf-8') + struct.pack('<I', len(chunk)))
                            await client.write(chunk)
                            if 'progress_func' in options and options['progress_func']:
                                options['progress_func'](total_size, sent_size)
                        await client.write(Signal.DONE.encode('utf-8') + struct.pack('<I', len(chunk)))
                        await client.receive_done()
                return await f(*args, **kwargs)

            return wrapper

        return decorator

    def pull(self, f):
        async def wrapper(*args, **kwargs):
            async with Client() as client:
                await client.call('host:transport:{}'.format(self.device.serial))
                # send sync signal
                await client.call('sync:')
                # send sync file info data
                arg = kwargs['src_path'].encode('utf-8')
                await client.write(Signal.RECV.encode('utf-8') + struct.pack('<I', len(arg)) + arg)
                # send data now
                async with aiofiles.open(kwargs['dest_path'], 'wb') as stream:
                    while True:
                        flag = (await client.reader.read(4)).decode('utf-8')

                        if flag == Signal.DONE:
                            await client.reader.read(4)
                            break

                        data_len = struct.unpack("<I", await client.reader.read(4))[0]
                        data = bytearray()
                        while len(data) < data_len:
                            data += await client.reader.read(data_len - len(data))

                        if flag == Signal.DATA:
                            await stream.write(data)

                        if flag == Signal.FAIL:
                            raise ConnectionError('pull data error: {}'.format(data.decode('utf-8')))

            return await f(*args, **kwargs)

        return wrapper


tp = Transport()


@tp.transport
class Device(object):

    def __init__(self, serial: str):
        self.serial = serial

    async def shell(self, command: str, pipeline=None):

        @tp.shell(command=command)
        async def run_cmd(pipeline_func):
            pass

        def parsing_result(line):
            if pipeline is not None:
                pipeline(line)

        await run_cmd(pipeline_func=parsing_result)

    async def push(self, src: str, dest: str, progress_func=None):
        if not os.path.exists(src):
            raise FileNotFoundError("Can't find the source file {}".format(src))

        @tp.push(progress_func=progress_func, mode=0o644)
        async def push_file(src_path, dest_path):
            pass

        if os.path.isfile(src):
            await push_file(src_path=src, dest_path=dest)
        else:
            for root, dirs, files in os.walk(src):
                root_dir_path = os.path.join(os.path.basename(src), root.replace(src, ''))
                await self.shell('mkdir -p {}/{}'.format(dest, root_dir_path))

                for sub_f in files:
                    await push_file(src_path=os.path.join(root, sub_f),
                                    dest_path=os.path.join(dest, root_dir_path, sub_f))

    async def pull(self, src: str, dest: str):
        @tp.pull
        async def pull_file(src_path, dest_path):
            pass

        await pull_file(src_path=src, dest_path=dest)

    async def list_package(self) -> List[str]:
        pkgs = []

        @tp.shell(command='pm list packages 2>/dev/null')
        async def list_pkgs(pipeline_func):
            pass

        def parsing_line(line):
            m = re.match("^package:(.*?)\r?$", line)
            if m:
                pkgs.append(m.group(1))

        await list_pkgs(pipeline_func=parsing_line)

        return pkgs

    async def get_properties(self) -> Dict[str, str]:
        properties = {}

        @tp.shell(command='getprop')
        async def getprop(pipeline_func):
            pass

        def parsing_line(line):
            m = re.match("^\[([\s\S]*?)\]: \[([\s\S]*?)\]\r?$", line)
            if m:
                properties[m.group(1)] = (m.group(2))

        await getprop(pipeline_func=parsing_line)

        return properties

    async def logcat(self, pipeline):
        @tp.shell(command='logcat')
        async def print_logcat(pipeline_func):
            pass

        await print_logcat(pipeline_func=pipeline)

    @staticmethod
    def __process_install(**kwargs):
        args_dict = {
            'forward_lock': '-l',
            'reinstall': '-r',
            'test': '-t',
            'installer_package_name': '-i',
            'shared_mass_storage': '-s',
            'internal_system_memory': '-f',
            'downgrade': '-d',
            'grand_all_permission': '-g'
        }

        args = []
        for k, v in args_dict.items():
            if k == 'installer_package_name' and kwargs[k]:
                args.append('-i {}'.format(v))
                continue
            if kwargs[k]:
                args.append(v)
        return ' '.join(args)

    async def install(self, path: str,
                      forward_lock: bool = False,
                      reinstall: bool = False,
                      test: bool = False,
                      installer_package_name: str = '',
                      shared_mass_storage: bool = False,
                      internal_system_memory: bool = False,
                      downgrade: bool = False,
                      grand_all_permission: bool = False):
        # push apk to temp first
        result = None
        dest_path = os.path.join('/data/local/tmp', os.path.basename(path))
        await self.push(path, dest_path)

        @tp.shell(command='pm install {} {}'.format(self.__process_install(**(locals())), cmd_quote(dest_path)))
        async def install_apk(pipeline_func):
            pass

        def parsing_result_f(line):
            print(line)
            nonlocal result
            result = re.search("(Success|Failure|Error)\s?(.*)", line)

        await install_apk(pipeline_func=parsing_result_f)

        if result and result.group(1) == "Success":
            return True
        elif result:
            groups = result.groups()
            raise RuntimeError("{} could not be installed - [{}]".format(dest_path, groups[1]))
        else:
            raise RuntimeError("{} could not be installed - [{}]".format(dest_path, result))

    async def is_installed(self, pkg_name: str) -> bool:
        result = False

        def parsing_result(line):
            nonlocal result
            result = 'package:' in line

        await self.shell('pm path {}'.format(pkg_name), pipeline=parsing_result)
        return result

    async def uninstall(self, pkg_name: str) -> bool:
        result = False

        def parsing_result(line):
            nonlocal result
            result = re.search("(Success|Failure.*|.*Unknown package:.*)", line)

        await self.shell('pm uninstall {}'.format(pkg_name), pipeline=parsing_result)
        if result and result.group(1) == "Success":
            return True
        return False
