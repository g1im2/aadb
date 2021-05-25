import asyncio
import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Task(object, metaclass=Singleton):

    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        self.event_loop: asyncio.AbstractEventLoop = event_loop

    def add_task(self, task_name):
        future = asyncio.run_coroutine_threadsafe(coro=None, loop=self.event_loop)
        future.result()

    async def run(self, timeout: int = 0):
        self.event_loop.call_later(delay=timeout, )

    def __end_callback(self, future: asyncio.Future):
        pass