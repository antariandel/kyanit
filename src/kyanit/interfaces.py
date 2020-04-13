# Kyanit (Core) - interfaces module
# Copyright (C) 2020 Zsolt Nagy
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>.


import utime
from network import WLAN
from network import AP_IF
from network import STA_IF

wlan = WLAN(STA_IF)
ap = WLAN(AP_IF)

wlan.active(False)
ap.active(False)


def wlan_connect(ssid, password, wait=True, timeout=10, ifconfig="dhcp"):
    wlan.active(True)
    wlan.ifconfig(ifconfig)
    wlan.connect(ssid, password)

    if wait:
        return wlan_wait_connected(timeout)

    return None


def wlan_wait_connected(timeout=10):
    if wlan.isconnected():
        return True

    timeout_future = utime.ticks_add(utime.ticks_ms(), timeout * 1000)
    while utime.ticks_diff(timeout_future, utime.ticks_ms()) > 0:
        if wlan.isconnected():
            return True

    return False
