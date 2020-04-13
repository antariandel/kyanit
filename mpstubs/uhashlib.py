if False:
    from typing import *  # noqa


class SHA256:
    def __init__(self, initial_data: bytes):
        ...

    def update(self, data: bytes):
        ...

    def digest(self) -> bytes:
        ...


def sha256() -> SHA256:
    ...
