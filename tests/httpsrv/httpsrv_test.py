# Kyanit (Core) - tests/httpsrv_test.py
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


import uos
import ujson
import uasyncio
from kyanit import httpsrv
from kyanit import interfaces

uos.stat("/wlan.json")
wlan_info = ujson.load(open("/wlan.json"))
ssid = wlan_info["ssid"]
password = wlan_info["password"]

if not interfaces.wlan_connect(ssid, password):
    raise Exception("can not connect to wlan")

print("IP is {}".format(interfaces.wlan.ifconfig()[0]))


def echo_request_info(mthd, loc, parms, hdrs, conn, addr):
    headers = "\n".join("  {}: {}".format(key, hdrs[key]) for key in hdrs)
    params = "\n".join("  {}: {}".format(key, parms[key]) for key in parms)

    body = httpsrv.readall_from(conn, timeout=0.25).getvalue().decode()

    response = (
        "{method} {loc} (from {ip})\n"
        "Headers:\n"
        "{headers}\n"
        "Query params:\n"
        "{params}\n"
        "Body:\n"
        "{body}"
    ).format(
        method=mthd, loc=loc, ip=addr[0], headers=headers, params=params, body=body
    )

    if "error" in parms:
        raise Exception("deliberate error")

    return httpsrv.response(
        200, body=response, headers={"Host": interfaces.wlan.ifconfig()[0]}
    )


httpsrv.init(80)
httpsrv.register("GET", "^/$", echo_request_info)
httpsrv.register("GET", ".*", echo_request_info)
httpsrv.register("PUT", ".*", echo_request_info)
httpsrv.register("POST", ".*", echo_request_info)
httpsrv.register("PATCH", ".*", echo_request_info)
httpsrv.register("DELETE", ".*", echo_request_info)

loop = uasyncio.get_event_loop()
loop.create_task(httpsrv.catch_requests())
loop.run_forever()
