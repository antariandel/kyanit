if False: from typing import *  # noqa


def pack(fmt, *args):
    # type: (str, Union[int, float, bytes]) -> bytes
    ...


def unpack(fmt, data):
    # type: (str, bytes) -> tuple
    ...
