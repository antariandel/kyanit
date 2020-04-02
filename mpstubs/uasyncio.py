if False: from typing import *  # noqa


class CancelledError(Exception):
    ...


class PollEventLoop:
    def create_task(self, coro_gen):
        # type: (Awaitable) -> None
        ...

    def call_soon(self, func, *args):
        # type: (Callable[..., Any], Any) -> None
        ...

    def call_later(self, func, *args):
        # type: (Callable[..., Any], Any) -> None
        ...

    def run_forever(self):
        # type: () -> None
        ...


def get_event_loop():
    # type: () -> PollEventLoop
    ...


def cancel(coro_gen):
    # type: (Awaitable) -> None
    ...


async def sleep(seconds):
    # type: (Union[int, float]) -> None
    ...


async def sleep_ms(seconds):
    # type: (int) -> None
    ...
