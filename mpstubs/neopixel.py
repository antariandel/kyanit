import machine

if False: from typing import *  # noqa


class NeoPixel:
    def __init__(self, pin, num_leds):
        # type: (machine.Pin, int) -> None
        ...

    def write(self):
        # type: () -> None
        ...

    def __getitem__(self, idx):
        # type: (int) -> Union[Tuple[int, int, int], List[int]]
        ...

    def __setitem__(self, idx, color):
        # type: (int, Union[Tuple[int, int, int], List[int]]) -> None
        ...
