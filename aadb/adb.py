from enum import Enum
from typing import List

from aadb.device import Device
from aadb.device import Transport

tp = Transport()


class AndroidDebugBridge(object):

    class DeviceStatus(Enum):
        OFFLINE = "offline"
        DEVICE = "device"
        BOOTLOADER = "bootloader"

    async def devices(self, state: DeviceStatus = None) -> List[Device]:
        device_list = []

        @tp.host(command='devices')
        async def list_devices(parsing_result):
            pass

        def parsing_result_f(result):
            for line in result.split('\n'):
                if not line:
                    break

                tokens = line.split()
                if state and len(tokens) > 1 and tokens[1] != state:
                    continue

                device_list.append(Device(tokens[0]))

        await list_devices(parsing_result=parsing_result_f)
        return device_list

    async def features(self):
        feature_list = []

        @tp.host(command='features')
        async def list_features(parsing_result):
            pass

        def parsing_result_f(result):
            feature_list.extend(result.split(','))

        await list_features(parsing_result=parsing_result_f)
        return feature_list

    async def version(self):
        ver = 0

        @tp.host(command='version')
        async def check_version(parsing_result):
            pass

        def parsing_result_f(result):
            nonlocal ver
            ver = int(result, 16)

        await check_version(parsing_result=parsing_result_f)
        return ver

    async def kill_server(self):
        @tp.host(command='kill', no_receive=False)
        async def kill_adb_server():
            pass

        await kill_adb_server()

    async def kill_forward_all(self):
        @tp.host(command='killforward-all', no_receive=False)
        async def kill_adb_server():
            pass

        await kill_adb_server()

    async def list_forward(self):
        forwards = {}

        @tp.host(command='list-forward')
        async def list_features(parsing_result):
            pass

        def parsing_result_f(result):
            for line in result.split('\n'):
                if line:
                    serial, local, remote = line.split()
                    if serial not in forwards:
                        forwards[serial] = {}

                    forwards[serial][local] = remote

        await list_features(parsing_result=parsing_result_f)
        return forwards

    async def remote_connect(self, host: str, port: int):
        request_result = False

        @tp.host(command='connect:%s:%d' % (host, port))
        async def connect_remote(parsing_result):
            pass

        def parsing_result_f(result):
            nonlocal request_result
            request_result = 'connected' in result

        await connect_remote(parsing_result=parsing_result_f)
        return request_result

    async def remote_disconnect(self, host: str = None, port: int = None):
        cmd = ''
        if host and port:
            cmd = '{}:{}'.format(host, port)
        if host and not port:
            cmd = host

        @tp.host(command='disconnect:{}'.format(cmd))
        async def disconnect_remote(parsing_result):
            pass

        def parsing_result_f(result):
            print(result)

        await disconnect_remote(parsing_result=parsing_result_f)
