import asyncio
from asyncio import StreamReader, StreamWriter
from asyncio import StreamReaderProtocol

import aadb
from aadb import events


class Signal(object):
    OKAY = 'OKAY'
    FAIL = 'FAIL'
    STAT = 'STAT'
    LIST = 'LIST'
    DENT = 'DENT'
    RECV = 'RECV'
    DATA = 'DATA'
    DONE = 'DONE'
    SEND = 'SEND'
    QUIT = 'QUIT'


class Stats(object):
    # The following constant were extracted from `man 2 stat` on Ubuntu 12.10.
    S_IFMT = 0o170000  # bit mask for the file type bit fields
    S_IFSOCK = 0o140000  # socket
    S_IFLNK = 0o120000  # symbolic link
    S_IFREG = 0o100000  # regular file
    S_IFBLK = 0o060000  # block device
    S_IFDIR = 0o040000  # directory
    S_IFCHR = 0o020000  # character device
    S_IFIFO = 0o010000  # FIFO
    S_ISUID = 0o004000  # set UID bit
    S_ISGID = 0o002000  # set-group-ID bit (see below)
    S_ISVTX = 0o001000  # sticky bit (see below)
    S_IRWXU = 0o0700  # mask for file owner permissions
    S_IRUSR = 0o0400  # owner has read permission
    S_IWUSR = 0o0200  # owner has write permission
    S_IXUSR = 0o0100  # owner has execute permission
    S_IRWXG = 0o0070  # mask for group permissions
    S_IRGRP = 0o0040  # group has read permission


class ClientProtocol(StreamReaderProtocol):

    def __init__(self, stream_reader: StreamReader, loop: asyncio.AbstractEventLoop):
        super().__init__(stream_reader, loop=loop)


class Client(object):

    def __init__(self):
        self.host = aadb.inner_host
        self.port = aadb.inner_port
        self.reader: StreamReader = None
        self.writer: StreamWriter = None
        self.transport = None

    async def __aenter__(self):
        self.reader = StreamReader(loop=events.get_event_loop())
        protocol = ClientProtocol(self.reader, loop=events.get_event_loop())
        try:
            self.transport, _ = await events.get_event_loop().create_connection(lambda: protocol, self.host, self.port)
            self.writer = StreamWriter(self.transport, protocol, self.reader, events.get_event_loop())
        except ConnectionRefusedError as e:
            print(e)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except AttributeError as e:
                print('close error:', e)

    async def call(self, request: str):
        request_encode = request.encode('utf-8')
        request_length = "{0:04X}".format(len(request_encode)).encode('utf-8')
        self.writer.write(b''.join([request_length, request_encode]))
        await self.writer.drain()
        return await self.receive_done()

    async def receive_done(self):
        status_data = await self.reader.read(4)
        if status_data.decode('utf-8') != Signal.OKAY:
            error = (await self.reader.read(1024)).decode('utf-8')
            print(error)
            raise ConnectionError('write error')

        return True

    async def receive(self):
        head_data = (await self.reader.read(4)).decode('utf-8')
        data_length = int(head_data, 16)
        return (await self.reader.read(data_length)).decode('utf-8')

    async def receive_lines(self, pipeline_func):
        temp_data = b''
        temp_line = ''
        while True:
            receive_data = temp_data + await self.reader.read(1024)
            try:
                result = receive_data.decode('utf-8')
                temp_data = b''
                if not result:
                    if temp_line:
                        pipeline_func(temp_line)
                    break
                result = temp_line + result
                lines = result.split('\n')
                if not result.endswith('\n'):
                    temp_line = lines.pop(-1)
                for line in lines:
                    if not line:
                        continue
                    pipeline_func(line)
            except UnicodeDecodeError:
                temp_data = receive_data

    async def write(self, data):
        self.writer.write(data)
