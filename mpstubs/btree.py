if False: from typing import *  # noqa

INCL = 0  # type: int
DESC = 0  # type: int


class BTree:
    def close(self):
        # type: () -> None
        ...
    
    def flush(self):
        # type: () -> None
        ...
    
    def __getitem__(self, key):
        # type: (bytes) -> bytes
        ...

    def __setitem__(self, key, val):
        # type: (bytes, bytes) -> None
        ...

    def __delitem__(self, key):
        # type: (bytes) -> None
        ...

    def __contains__(self, key):
        # type: (bytes) -> bool
        ...

    def get(self, key, default=None):
        # type: (bytes, Optional[bytes]) -> Optional[bytes]
        ...

    def __iter__(self):
        # type: () -> BTree
        ...
    
    def __next__(self):
        # type: () -> bytes
        ...

    def keys(self, start_key=None, end_key=None, flags=None):
        # type: (Optional[bytes], Optional[bytes], Optional[int]) -> Iterable[bytes]
        ...

    def values(self, start_key=None, end_key=None, flags=None):
        # type: (Optional[bytes], Optional[bytes], Optional[int]) -> Iterable[bytes]
        ...

    def items(self, start_key=None, end_key=None, flags=None):
        # type: (Optional[bytes], Optional[bytes], Optional[int]) -> Iterable[Tuple[bytes, bytes]]
        ...


def open(stream, flags=0, pagesize=0, cachesize=0, minkeypage=0):
    # type: (BinaryIO, int, int, int, int) -> BTree
    ...
