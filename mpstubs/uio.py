if False: from typing import *  # noqa


class StringIO:

    def __init__(self, alloc_size=0):
        # type: (int) -> None
        ...

    def getvalue(self):
        # type: () -> str
        ...


class BytesIO:

    def __init__(self, alloc_size=0):
        # type: (int) -> None
        ...

    def getvalue(self):
        # type: () -> bytes
        ...
