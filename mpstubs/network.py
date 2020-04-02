if False: from typing import *  # noqa

STA_IF = 0  # type: int
AP_IF = 0  # type: int


class WLAN:
    def __init__(self, interface):
        # type: (int) -> None
        ...

    def active(self, active=None):
        # type: (Optional[bool]) -> None
        ...

    def connect(self, ssid, password):
        # type: (str, str) -> None
        ...

    def isconnected(self):
        # type: () -> bool
        ...

    def ifconfig(self):
        # type: () -> Tuple[str, str, str, str]
        ...
