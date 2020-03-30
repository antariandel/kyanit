# Kyanit (Core) - __init__ module
# Copyright (C) 2020 Zsolt Nagy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import gc
import uos
import ure
import ujson
import network
import machine
import neopixel
import ubinascii

from . import colorid
from . import runner
from . import httpsrv
from . import interfaces


LEDS_PIN = 4
BUTTON_PIN = 14


__version__ = '0.1.0'
_color_id = None


class StoppedError(Exception):
    pass


class RebootError(Exception):
    pass


class ResetError(Exception):
    pass


class FileServerError(Exception):
    pass


class Netvar:
    _in = None
    _out = None

    @staticmethod
    def inbound(obj=None, clear=False):
        if clear:
            Netvar._in = None
            return
        
        if obj is None:
            return Netvar._in
        
        Netvar._in = obj
    
    @staticmethod
    def outbound(obj=None, clear=False):
        if clear:
            Netvar._out = None
            return
        
        if obj is None:
            return Netvar._out
        
        Netvar._out = obj


def get_color_id():
    return _color_id


def get_fallback_ap_settings():
    # generate unique name for AP SSID
    flash_id = ubinascii.hexlify(machine.unique_id()).upper().decode()
    return {
        'ssid': 'Kyanit {}'.format(flash_id[:4]),
        'password': 'myKyanit'
    }


def controls(active_colors=((0, 250, 200), ) * 3, idle_colors=((250, 50, 0), ) * 3):
    from . import neoleds
    from . import button

    front_leds = neoleds.NeoLeds(pin_number=LEDS_PIN, num_leds=3)
    front_button = button.Button(pin_number=BUTTON_PIN, invert=True)

    async def show_id_on_leds():
        while True:
            if front_button.check() == 'click':
                front_leds.display(utils.id_to_colors(get_color_id()), time=10)
            await runner.sleep_ms(100)
    
    def decorator(func):
        # wrapper for code.main and code.cleanup
        def wrapper(*args):
            runner.create_task('neoleds', front_leds.display_task)
            runner.create_task('button', front_button.checker_task)
            runner.create_task('show_id', show_id_on_leds)
            if not args:
                front_leds.display(active_colors, neoleds.Animations.breathe, anim_speed=10)
            elif args[0] is StoppedError:
                front_leds.display(idle_colors, neoleds.Animations.breathe, anim_speed=5)
            elif args[0] is not RebootError and args[0] is not ResetError:
                front_leds.display(idle_colors, neoleds.Animations.attention, anim_speed=10)
            func(*args)
        return wrapper
    return decorator


def run():
    global _color_id

    PROTECTED_FILES = ['main.py', 'boot.py', '_boot.py']

    def setup_fallback_ap():
        ap_settings = get_fallback_ap_settings()
        interfaces.ap.active(True)
        interfaces.ap.config(essid=ap_settings['ssid'],
                             password=ap_settings['password'],
                             authmode=network.AUTH_WPA_WPA2_PSK)
    
    async def front_leds_blink(neop, color):
        # when fallback AP is active
        trigger = True
        while True:
            for i in range(3):
                if trigger:
                    neop[i] = color
                else:
                    neop[i] = (0, 0, 0)
            neop.write()
            trigger = not trigger
            await runner.sleep_ms(500)
    
    async def check_wlan_connection():
        global _color_id

        while True:
            await runner.sleep(30)
            if not interfaces.wlan.isconnected():
                _color_id = 'BBB'
            elif _color_id == 'BBB':
                _color_id = colorid.from_number(
                    int(ure.search('\d+$', interfaces.wlan.ifconfig()[0]).group(0))  # noqa
                )
    
    fallback_ap_mode = False
    button = machine.Signal(machine.Pin(BUTTON_PIN, machine.Pin.IN), invert=True)
    if button.value():
        fallback_ap_mode = True
    # try connecting wlan
    try:
        if fallback_ap_mode:
            raise Exception  # skip to setting up AP
        wlan_info = ujson.load(open('/wlan.json'))
        ssid = wlan_info['ssid']
        password = wlan_info['password']
        ifconfig = wlan_info['ifconfig'] if 'ifconfig' in wlan_info else 'dhcp'
    except Exception:
        # set up AP, if can't get JSON, or malformed
        fallback_ap_mode = True
        setup_fallback_ap()
    else:
        if not interfaces.wlan_connect(ssid, password, ifconfig=ifconfig, timeout=20):
            # set up AP, if can't connect
            interfaces.wlan.active(False)
            fallback_ap_mode = True
            setup_fallback_ap()
    if fallback_ap_mode:
        neop = neopixel.NeoPixel(machine.Pin(LEDS_PIN), 3)
        loop = runner.get_event_loop()
        loop.create_task(front_leds_blink(neop, (0, 0, 255)))

    # set Color ID based on last octet of IP address
    _color_id = colorid.from_number(
        int(ure.search('\d+$', interfaces.wlan.ifconfig()[0]).group(0))  # noqa
    )

    def action_file_list(*args):
        return httpsrv.response(
            200,
            ujson.dumps([path for path in uos.listdir('/')
                        if uos.stat(path)[0] == 32768 and path not in PROTECTED_FILES]),
            httpsrv.CT_JSON)

    def action_files(method, loc, params, headers, conn, addr):
        if '/' in loc[7:]:  # only files in root dir are allowed
            raise FileServerError('not on root')

        file_name = loc[6:]
        
        if file_name in PROTECTED_FILES:
            raise FileServerError('restricted')
        
        try:
            stat = uos.stat(file_name)
        except OSError:
            if method == 'GET' or method == 'DELETE' or 'rename' in params:
                return httpsrv.response(404, '"File Not Found"', httpsrv.CT_JSON)
        else:
            if stat[0] != 32768:
                raise FileServerError('restricted')
        
        if method == 'DELETE':
            uos.remove(file_name)
            return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)
        
        if method == 'GET':
            with open(file_name, 'rb') as file:
                # read from file, send to conn
                httpsrv.send_response(conn,
                                      **(httpsrv.response(200, content_type=httpsrv.CT_PLAIN)))
                httpsrv.readall_from(file, into=conn)
            return None  # response already assembled above
        
        elif method == 'PUT':
            if 'rename' in params:
                uos.rename(file_name, params['rename'])
                return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)
            
            with open(file_name, 'wb') as file:
                # write to file, receive from conn
                httpsrv.readall_from(conn, into=file)
            return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)
    
    async def reboot(hard=True, delay=1):
        await runner.sleep(delay)
        if hard:
            raise RebootError
        else:
            raise ResetError

    def action_reboot(method, loc, params, headers, conn, addr):
        # TODO: Remove this if statement once working.
        if 'soft' in loc:
            raise ValueError('soft reset not yet supported')
        runner.stop(exc=ResetError if 'soft' in loc else RebootError)
        runner.get_event_loop().create_task(reboot(False if 'soft' in loc else True))
        return httpsrv.response(200, '"OK"', 'application/json')

    def action_state(method, loc, params, headers, conn, addr):
        return httpsrv.response(200, ujson.dumps({
            'firmware_version': __version__,
            'color_id': _color_id,
            'free_memory': gc.mem_free(),
            'free_flash': uos.statvfs('/')[0] * uos.statvfs('/')[3],
            'run_state':
                ['ERROR {}'.format(runner.get_error()[0]) if runner.get_error() is not None else '',
                 'STOPPED', 'CODE.PY MISSING', 'CODE.PY IMPORTED', 'CODE.PY MAIN'][
                     runner.get_state()],
            'error_traceback': [line.strip() for line in runner.get_error()[1].split('\n')
                                if line and 'Traceback' not in line]
                               if runner.get_error() is not None else None  # noqa
        }), 'application/json')

    def action_runner_start(method, loc, params, headers, conn, addr):
        runner.start()
        return httpsrv.response(200, '"OK"', 'application/json')

    def action_runner_stop(method, loc, params, headers, conn, addr):
        runner.stop(force=True if 'force' in loc else False, exc=StoppedError)
        return httpsrv.response(200, '"OK"', 'application/json')
    
    def action_netvar(method, loc, params, headers, conn, addr):
        if method == 'POST':
            Netvar.inbound(ujson.loads(httpsrv.readall_from(conn).getvalue().decode()))
            return httpsrv.response(200, '"OK"', 'application/json')
        if method == 'GET':
            return httpsrv.response(200, ujson.dumps(Netvar.outbound()), 'application/json')

    # Set up HTTP server on port 3300
    http_server = httpsrv.HTTPServer(3300)
    httpsrv.add_status(404, 'Not Found')

    # File actions
    http_server.register('GET', '^/files$', action_file_list)
    http_server.register('GET', '^/files/$', action_file_list)
    http_server.register('GET', '^/files/.*', action_files)
    http_server.register('PUT', '^/files/.*', action_files)
    http_server.register('DELETE', '^/files/.*', action_files)

    # System actions
    http_server.register('GET', '^/sys/state$', action_state)
    http_server.register('POST', '^/sys/reboot$', action_reboot)
    http_server.register('POST', '^/sys/reboot/soft$', action_reboot)

    # Runner actions
    http_server.register('POST', '^/sys/start$', action_runner_start)
    http_server.register('POST', '^/sys/stop$', action_runner_stop)
    http_server.register('POST', '^/sys/stop/force$', action_runner_stop)

    # Netvar actions
    http_server.register('GET', '^/netvar$', action_netvar)
    http_server.register('POST', '^/netvar$', action_netvar)

    # Run
    loop = runner.get_event_loop()
    loop.create_task(http_server.catch_requests())
    # do not start automatically on fallback
    if not fallback_ap_mode:
        loop.create_task(check_wlan_connection())
        loop.create_task(runner.starter_coro())
    loop.run_forever()
