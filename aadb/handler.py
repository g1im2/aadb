from abc import abstractmethod
from device import Client


class ChunkHandler(object):

    CHUNK_HEADER_LEN = 8
    CHUNK_ORDER = ByteOrder.BIG_ENDIAN

    CHUNK_FAIL = type("FAIL")

    @abstractmethod
    def client_ready(self, client: Client):
        pass

    @abstractmethod
    def client_disconnected(self, client: Client):
        pass

    @abstractmethod
    def handle_chunk(self, client: Client, c_type: int, ):