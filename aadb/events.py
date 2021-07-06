import asyncio
import threading
from asyncio import AbstractEventLoop

_lock = threading.Lock()

_event_loop_policy: 'DefaultPolicy' = None


class DefaultPolicy(object):
    class _Local(object):
        _loop: AbstractEventLoop = None
        _called = False

    def set_event_loop(self, loop: AbstractEventLoop):
        self._Local._called = True
        self._Local._loop = loop

    def get_event_loop(self) -> AbstractEventLoop:
        if self._Local._loop is None and not self._Local._called:
            self.set_event_loop(asyncio.new_event_loop() if threading.current_thread() != threading.main_thread()
                                else asyncio.get_event_loop())
        return self._Local._loop


def _init_event_loop_policy():
    global _event_loop_policy
    with _lock:
        if _event_loop_policy is None:
            _event_loop_policy = DefaultPolicy()


def get_event_loop_policy() -> DefaultPolicy:
    if _event_loop_policy is None:
        _init_event_loop_policy()
    return _event_loop_policy


def get_event_loop() -> AbstractEventLoop:
    return get_event_loop_policy().get_event_loop()


def set_event_loop(loop: AbstractEventLoop):
    get_event_loop_policy().set_event_loop(loop)
