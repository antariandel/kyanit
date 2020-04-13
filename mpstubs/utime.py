if False:
    from typing import *  # noqa


def sleep(seconds):
    # type: (Union[int, float]) -> None
    ...


def sleep_ms(milliseconds):
    # type: (int) -> None
    ...


def sleep_us(microseconds):
    # type: (int) -> None
    ...


def ticks_ms():
    # type: () -> int
    ...


def ticks_us():
    # type: () -> int
    ...


def ticks_cpu():
    # type: () -> int
    ...


def ticks_add(ticks, delta):
    # type: (int, int) -> int
    ...


def ticks_diff(ticks1, ticks2):
    # type: (int, int) -> int
    ...


def localtime(secs=None):
    # type: (int) -> Tuple[int, int, int, int, int, int, int, int]
    ...


def time():
    # type: () -> int
    ...


def mktime(time_tuple):
    # type: (Tuple[int, int, int, int, int, int, int, int]) -> int
    ...
