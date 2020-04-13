if False:
    from typing import *  # noqa


class Pin:
    IN = 0  # type: int
    OUT = 0  # type: int

    IRQ_RISING = 0  # type: int
    IRQ_FALLING = 0  # type: int

    PULL_UP = 0  # type: int
    OPEN_DRAIN = 0  # type: int

    def __init__(self, id, mode=-1, pull=-1):
        # type: (int, int, int) ->None
        ...

    def init(self, mode=-1, pull=-1):
        # type: (int, int) ->None
        ...

    def irq(
        self,
        handler=None,
        trigger=(IRQ_FALLING | IRQ_RISING),
        priority=1,
        wake=None,
        hard=False,
    ):
        # type: (Optional[Callable[[Pin], Any]], int, int, Optional[int], bool) -> None
        ...

    def value(self, x=None):
        # type: (Optional[bool]) -> Optional[bool]
        ...

    def on(self):
        # type: () -> None
        ...

    def off(self):
        # type: () -> None
        ...


class Signal:
    def __init__(self, pin_obj, invert=False):
        # type: (Pin, bool) -> None
        ...

    def value(self, x=None):
        # type: (Optional[bool]) -> Optional[bool]
        ...

    def on(self):
        # type: () -> None
        ...

    def off(self):
        # type: () -> None
        ...


class WDT:
    def feed(self):
        # type: () -> None
        ...


class RTC:
    def datetime(self, time_tuple):
        # type: (Tuple[int, int, int, int, int, int, int, int]) -> None
        ...


def reset_cause():
    # type: () -> int
    ...


def reset():
    # type: () -> None
    ...


def soft_reset():
    # type: () -> None
    ...
