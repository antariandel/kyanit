if False: from typing import *  # noqa


AF_INET = 0  # type: int
AF_INET6 = 0  # type: int

SOCK_STREAM = 0  # type: int
SOCK_DGRAM = 0  # type: int

IPPROTO_UDP = 0  # type: int
IPPROTO_TCP = 0  # type: int


def getaddrinfo(host, port, af=0, type=0, proto=0, flags=0):
    # type: (str, int, int, int, int, int) -> List[Tuple[int, int, int, str, Tuple[str, int]]]
    ...


class socket:

    def __init__(self, af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
        # type: (int, int, int) -> None
        ...

    def close(self):
        # type: () -> None
        ...

    def settimeout(self, value):
        # type: (int) -> None
        ...

    def sendto(self, bytes, address):
        # type: (bytes, Tuple[str, int]) -> int
        ...

    def recv(self, bufsize):
        # type: (int) -> bytes
        ...
