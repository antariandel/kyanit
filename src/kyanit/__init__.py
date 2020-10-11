# Kyanit (Core) - __init__ module
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

"""
# Kyanit Core

The `kyanit` package is referred to as Kyanit Core.

Kyanit Core is a user code supervisor built for MicroPython. Development is currently
focused on the ESP8266 port of MicroPython. Together with an ESP8266-based board, Kyanit
Core is indended to be a foundation for home automation systems. A board with Kyanit
Core installed is referred to simply as Kyanit or Kyanit board. An official board design
for Kyanit can be found at https://kyanit.eu/kyanit-board.

For information about MicroPython head to https://micropython.org/

Being a supervisor, Kyanit Core is responsible for starting and stopping user code, as
well as handling any uncaught exceptions in the user code.

Kyanit Core provides an HTTP API through which the user code can be changed and
controlled. Additionally it provides an addressing mechanism called the "Color ID,"
which maps to the IP address of the board. The Color ID consists of 3 colors, each
either red, gree, blue, cyan, magenta, yellow or white, and they are displayed using 3
WS2812B (Neopixel) LEDs.

The official board design already has these LEDs built in, as well as a button, which
when pressed, will make the Color ID be displayed on the LEDs.

## The Kyanit Ecosystem

* [**Kyanit Core**](https://kyanit-project.github.io/kyanit/kyanit/)

The core Kyanit package, flashed into an ESP8266.

* [**Kyanit Board**](https://kyanit.eu/kyanit-board)

A stylish, triangle-shaped ESP8266-based board built around an ESP-12F module, the
official Kyanit board.

* [**Kyanit CTL**](https://kyanit-project.github.io/kyanit-ctl/kyanitctl/)

Command-line utility for interfacing and interacting with a Kyanit board.

* [**Kyanit API**](https://kyanit-project.github.io/kyanit-api/kyanitapi/)

Python API for interfacing and interacting with a Kyanit board from Python code.
(Kyanit CTL is an application of this API.)

## Getting Started with Kyanit Core

### Setting Up

The Kyanit Core package is intended to be compiled into the MicroPython firmware, and
flashed into an ESP8266. A board with at least 1 MB of flash is recommended, leaving
approximately 380 kB free for user code. The Kyanit Board, or any other board with an
ESP-12E/F is a good candidate. If you will not be working with the Kyanit Board, wire 3
WS2812B LEDs to Pin(4), and an active-low button to Pin(14) on your board of choice.
Other pin numbers are possible, in that case, some configuration is required, for
changing the pin numbers, see `kyanit.controls`.

If you're new to the WS2812B LEDs, you can refer to this extensive tutorial on SparkFun:
https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all

NOTE: It is possible to use the core package without flashing it into the firmware, but
substantially less RAM will be available (~5k versus ~20k).

To flash a released version into an ESP8266, see the [*Flashing a Released version of
Kyanit Core*](#flashing-a-released-version-of-kyanit-core) section further below.
Alternatively you can build the current development version, in that case, see
[*Building Kyanit Core from Source (Linux)*](#building-kyanit-core-from-source-linux).

The first time you power up the board, it will set up an AP with an SSID starting with
`Kyanit` and ending with a unique hexadecimal number. When the AP is active, the LEDs
will flash blue.

A command-line utility called `kyanitctl` is provided for managing a Kyanit board.
To start interacting with the board, install it from PyPI with:

```
pip install kyanitctl
```

Make sure you don't have a 192.168.4.0/24 network currently active in your system, as
this is the network address Kyanit will use while setting up. If you have an existing
network with this address, disconnect it first.

Connect to Kyanit's SSID, with the password `myKyanit`. Then start setting up Kyanit to
connect to your home wireless LAN, with DHCP enabled by executing:

```
kyanitctl -setup
```

Follow the instructions and enter your home network SSID and password. You can review
your settings before it gets uploaded to the board.

Alternatively you can set up a static IP configuration by running the setup with:

```
kyanitctl -setupstatic
```

Choose an IP address that's outside of the DHCP pool of your router. If you're unsure,
use `-setup` instead.

Kyanit will then reboot and try to connect to your wireless router. If this doesn't
work, it will fall back to AP, and start flashing the LEDs again. You can retry the
above steps, if this happens.

On successful connection, the LEDs will light up in a blueish color, with a slow
"breathing" animation. If you were originally connected to your home network through
wireless on your computer, you can now reconnect.

### The Color ID

Addressing a Kyanit board can be done in two ways. Either by knowing its IP address, or
by means of the Color ID. The Color ID is a sequence of 3 colors, each color being one
of red, green, blue, cyan, magenta, yellow or white:

<center>
<img width="100%" src="color_id_colors.svg" alt="All Color ID Colors"
style="max-width: 800px">
</center>

If you know the Color ID of the Kyanit, you don't need to know its IP address. To find
out the Color ID, press the button on the Kyanit. This will cause the Color ID to be
shown on the LEDs for 10 seconds.

On a Kyanit Board, the Color ID must be read starting from the bottom (where the USB
connector is), and going counter-clockwise, as the notches on the enclosure suggest.
Here are some Color ID examples:

<center>
<img width="100%" src="color_id_examples.svg" alt="Color ID Examples"
style="max-width: 800px">
</center>

The last octet of the IP address maps to the Color ID under the hood. For this reason
only networks with a subnet mask of 255.255.255.0 are supported. Most home and small
business routers create such a network, so you should be fine.

In the unlikely scenario where your home wireless network is configured with a netmask
different from 255.255.255.0, you'll need to provide the IP address of the Kyanit when
running `kyanitctl`. In that case it's easier if Kyanit is set up with a static IP.

Kyanit CTL will discover the networks available on your computer the first time you run
it with a Color ID. If one supported network is present on your system, it will be used
by default, otherwise you will be presented with a list of networks, and you'll need to
select the network, the Kyanit is connected to. The selection will be saved and used for
all further connection attempts. The network selection can be re-run with
`kyanitctl -reset_network` if desired later.

### Checking the status of the Kyanit

Try running `kyanitctl <Color ID> -status` (or `-stat` for short) to see the current
status of the board. Pass in the Color ID of your board to `<Color ID>` after checking
it by pressing the button.

Here's an example output for a Kyanit Board with a Color ID of BCG (Blue-Cyan-Green) on
a system where two supported networks are present:

```
> kyanitctl BCG -stat

=== Network Setup ===

Connecting to Kyanit with the Color ID works on networks with a netmask of 255.255.255.0
(most home wireless networks). Multiple such networks detected. Select the one Kyanit is
connected to:

0: 192.168.137.0   Ethernet
1: 192.168.1.0     Wi-Fi

Select network [0, 1]: 1
Saved. You may re-run this setup with -reset_network.

=== Kyanit BCG (192.168.1.9 through 'Wi-Fi') ===

Retrieving system status...

    Firmware version: 0.1.0
          Free flash: 3514368
         Free memory: 15776
           Run state: CODE.PY MAIN

```

Having the network saved, further runs will provide a much concise output:

```
=== Kyanit BCG (192.168.1.9 through 'Wi-Fi') ===

Retrieving system status...

    Firmware version: 0.1.0
          Free flash: 3514368
         Free memory: 18800
           Run state: CODE.PY MAIN
```

The same as above with IP address instead of the Color ID would be:

```
kyanitctl -ip 192.168.1.9 -stat

...
```

### Downloading and Uploading Files

List the files currently on the board with the `-files` option:

```
> kyanitctl BCG -files

=== Kyanit BCG (192.168.1.9 through 'Wi-Fi') ===

Retrieving file list done.
Files on Kyanit:

wlan.json
code.py

```

With a fresh install, you should see `wlan.json`, which includes your wireless
credentials and IP settings, and `code.py`, which is the user code that was uploaded as
part of the initial setup. This is the user code entry point. On startup, Kyanit Core
will try to import it and call the `main` function inside. The code currently only
controls the LEDs and monitors the button.

Download `code.py` from the board using `kyanitctl` with the option `-get code.py`.
(Be aware, that this will overwrite any existing `code.py` file that you may have in
your local directory.)

The `code.py` initially contains the following:

```python
# This code is imported on startup, then main is called, if it exists. Neither main, nor
# cleanup should block for too long. Use coroutines through
# kyanit.runner.create_task('name', coro) for continuous or longer tasks. Any errors
# (including from coroutines) will be passed to cleanup.
# The @kyanit.controls() decorator adds functionality to the LEDs and button. It can be
# removed if this is not required, to save ~1k of RAM.

# To get started, read more at https://kyanit.eu


import kyanit


@kyanit.controls()
def main():
    # Put startup code here.
    pass


@kyanit.controls()
def cleanup(exception):
    # Put error-handling code here, as well as code that needs to be run when stopped,
    # or before reboot.
    pass
```

The `kyanit.controls()` decorator on the `main` and `cleanup` functions should be left
there, unless you don't need feedback on run state (discussed in the next section) and
the Color ID. This means, that if you remove those, the Kyanit will be unresponsive to
button press, and the LEDs will not be controlled automatically.

Uploading a new `code.py` can be done with `-put code.py`. Other files can also be
uploaded, but keep in mind, that directories are not supported on Kyanit.
If you pass a directory to `-put`, every file from that directory will be uploaded
(and it will not recurse to further directories inside).

NOTE: The board will need to be rebooted with `-reboot` for the new code to become
active. This can be done with a single command, for example:

```
kyanitctl BCG -put code.py -reboot
```

For a full list of what Kyanit CTL can do, refer to the command-line help with
`kyanitctl -h`.

### Run States

There are 5 different run states: `CODE.PY MISSING`, `CODE.PY IMPORTED`, `CODE.PY MAIN`,
`STOPPED` and `ERROR`.

* **`CODE.PY MISSING`**

There's no `code.py` file to import and run.

* **`CODE.PY IMPORTED`**

There is a `code.py`, that was imported, but there's no `main` function in it to call.

* **`CODE.PY MAIN`**

`code.py` was imported, and `main` was called. This is what can be considred a "running"
state.

Having the `kyanit.controls()` decorator on `main` will make the LEDs "breathe" in a
bluish color, indicating that `main` was called, and that Kyanit is running the user
code.

* **`STOPPED`**

The code was stopped either from within the code itself, or by outside means, ex. with
Kyanit CTL's `-stop` option. The code may be restarted with Kyanit CTL, using the
`-start` option.

Before enterint this state, the runner will call the `cleanup` function. Having the
`kyanit.controls()` decorator on `cleanup` will change the LED colors to a deep orange,
and the animation will slow down, indicating that it entered the `STOPPED` state.

* **`ERROR ExceptionName`**

There was an uncaught exception within `code.py`. An exception detail, with traceback
will also be available through Kyanit CTL's `-status` option. At this point, the code
may be restarted. (Although debugging is probably required.)

Before enterint this state, the runner will call the `cleanup` function and it will pass
it the exception, so handling it is possible in `cleanup`. Having the
`kyanit.controls()` decorator on `cleanup` will change the LED colors to a deep orange,
and the animation will be a blinking "attention" animation, indicating that an uncaught
error occurred.

## Coding on Kyanit (Using Coroutines)

Kyanit Core is built around MicroPython's uasyncio. (CPython's asyncio implementation
for MicroPython.) This means Kyanit is all about coroutines. Albeit it's advisable to
learn about coroutines before coding on Kyanit, it's not entirely required, if you abide
by some basic rules.

A coroutine is just a function defined with `async`:

```python
async def my_func():
    # This is a coroutine
    pass
```

Coroutines are not multithreaded, but they can be understood as if they were running
alongside each other in parallel.

Every internal functionality of Kyanit is built using coroutines. This means, that your
code in `code.py` must also use coroutines to achieve continuous functionality. Nothing
within `code.py` should block for too long, because this essentially freezes the whole
system, preventing Kyanit from running its internal tasks, rendering it unresponsive.

In short, this means no continuous loops (with `while True`) within any non-async
functions, which includes `main` and `cleanup`.

`main` is intended to set up your own code and potentially start coroutines, which will
run alongside Kyanit's internal tasks.

Likewise, `cleanup` is intended to run quickly after some exception, potentially acting
on them.

`cleanup` is also called when code is stopped or rebooted, with `kyanit.StoppedError`
and `kyanit.RebootError` passed respectively. This lets you do stuff on these two
events, if desired.

Here's a simple example of a continuosly running task in `code.py`:

```python
from kyanit import controls, runner


async def my_task():
    while True:
        # do some stuff
        await runner.sleep(1)


@controls()
def main():
    runner.create_task('my_task_name', my_task)


@controls()
def cleanup(exception):
    pass
```

The above code will immediately start `my_task`. Note the `await` statement, which will
give CPU time for other coroutines to run. In this case, the uasyncio scheduler will
return to `my_task` after 1 second. You must have an `await` statement inside your
coroutines to yield CPU time to other tasks. You may also `await` other coroutines that
you defined.

**You may await a sleep time of 0**, which basically means "return to this function as
soon as possible." The scheduler will give time to other tasks that are not awaiting a
sleep in a round-robin fashion, and will return to the function as soon as possible.

HINT: Everything from uasyncio is available in `runner` (it has everything imported from
`uasyncio`).

### About `runner.create_task()`

The `kyanit.runner` module is responsible for running the code and keeping tabs on the
tasks.

Always create tasks with `runner.create_task()` from `runner` and not
`uasyncio.get_event_loop().create_task()`, because Kyanit can not catch errors in tasks
created on the event loop directly. Uncaught errors will cause the coroutine that's
raising them to stop silently, which may result in unexpected behavior.

On the other hand, errors in tasks created on the runner will be handled. In case of an
error, all tasks will be stopped in a controlled fashion, and Kyanit will go into ERROR
state. (See [*Run States*](#run-states) above.)

The same applies when running is stopped with `kyanit.runner.stop()` or by ex. Kyanit
CTL, using `-stop`. Kyanit will stop all tasks created on runner, but it cannot stop
tasks directly created on the event loop.

Stop a single task from running with `runner.destroy_task('task_name')`.

### The things to keep in mind:

* If you want a long-running code or continuous loop, implement it in an `async`
function and use `await runner.sleep()` where pauses can be accepted.
* Never use `time.sleep()` for long delays, use `await runner.sleep()` instead.
* If timing is critical (ex. for bit-banging), you may use `time.sleep()`, but keep in
mind that this prevents other coroutines to run in the meantime, so keep it short.
* Always create tasks with `runner.create_task()` from `runner`.

More on coroutines in MicroPython:
https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md

Read documentation of `kyanit.runner` to find out more about tasks and how to control
the runner.

## Additional sub-modules

Kyanit Core has the following sub-modules available:

* **`kyanit.button`**

Module to monitor a button and catch button events.

* **`kyanit.httpsrv`**

A minimal HTTP server module.

* **`kyanit.interfaces`**

Module to control the wireless network interfaces of the ESP8266.

* **`kyanit.neoleds`**

Module to control WS2812B LEDs (NeoPixels) with animations and different color display
options.

* **`kyanit.runner`**

The code executor and supervisor module.

* **`kyanit.colorid`**

Color ID helper functions.

All of these modules are available for the user code. Check out their documentation page
to see what they can do.

## Kyanit Netvar

Kyanit Core has a notion of a "network variable"which is available to read and write
through the network connection by Kyanit CTL or Kyanit API.

The Netvar can be used to issue custom commands to your board, such as switching or
reading some data from your board (like sensor data).

Check out the `kyanit.Netvar` class for details.

# Kyanit API

So far it was demonstrated how Kyanit CTL can be used to control a Kyanit board. If you
want to control your board from Python code, check out Kyanit API at
https://kyanit-project.github.io/kyanit-api/kyanitapi/.

# Flashing a Released version of Kyanit Core

Download the latest `kyanit-core-<version>.bin` from
https://github.com/kyanit-project/kyanit/releases/latest , then refer to MicroPython
documentation on flashing firmware onto an ESP8266 here:
https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

# Building Kyanit Core from Source (Linux)

To find out how to build from source, head to
https://github.com/kyanit-project/kyanit#building-from-source-linux

# License Notice

Copyright (C) 2020 Zsolt Nagy

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, version
3 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this
program. If not, see <https://www.gnu.org/licenses/>.

The above license notice applies to all parts of this package.
"""


import gc

import esp
import uos
import ure
import ujson
import machine
import network
import neopixel
import uhashlib
import ubinascii

from . import runner
from . import colorid
from . import httpsrv
from . import interfaces

if esp.flash_user_start() is not None:
    hasher = uhashlib.sha256()
    for i in range(esp.flash_user_start() / 1024):
        hasher.update(esp.flash_read(i * 1024, 1024))
    fw_digest = ubinascii.hexlify(hasher.digest()).decode()[:8]
else:
    fw_digest = "0"

try:
    from ._version import __version__  # noqa

    __version = "{}+{}".format(__version__, fw_digest)
except ImportError:
    __version__ = "build+{}".format(fw_digest)


LEDS_PIN = 4
BUTTON_PIN = 14


_color_id = None


class StoppedError(Exception):
    """
    This exception is passed to `code.cleanup` on a `stop` request through Kyanit API or
    Kyanit CTL.

    NOTE: Calling runner.stop() directly will not cause this exception to be passed to
    cleanup.
    """

    pass


class RebootError(Exception):
    """
    This exception is passed to `code.cleanup` on a `reboot` request through Kyanit API
    or Kyanit CTL.
    """

    pass


# class ResetError(Exception):
#     """
#     This exception is passed to `code.cleanup` on a `reset` request through Kyanit API
#     or Kyanit
#     CTL.
#     """
#     pass


class Netvar:
    """
    The Netvar is a notion of a "network variable", which is available to read and write
    through the network connection. Netvar is a static class, therefore it's not
    intended to be instantiated.

    There are 2 variables within Netvar, which can be understood as "channels".

    `Netvar.inbound()` accesses the variable that is written from "outside", such as by
    Kyanit CTL or Kyanit API.

    `Netvar.outbound()` on the other hand is what Kyanit publishes, and is available for
    reading by Kyanit CTL or Kyanit API.

    Both methods have the same usage. Having no parameters passed gets the actual value
    of the variables:

    ```python
    Netvar.inbound()  # gets the value of the inbound variable
    Netvar.outbound()  # gets the value of the outbound variable
    ```
    Passing an object sets the value:

    ```python
    Netvar.outbound('some_value')  # the outbound variable is now equal to 'some_value'
    ```

    Any object may be passed, which are JSON serializable.

    The inbound variable may also be written:

    ```python
    Netvar.inbound('processed')  # the new value is now 'processed'
    ```

    As suggested by the example, the inbound variable might be overwritten when the data
    (or part of it) has been processed.

    It is also possible to clear the variables with:

    ```python
    Netvar.inbound(clear=True)  # inbound now equals to None
    Netvar.outbound(clear=True)  # outbound now equals to None
    ```

    Kyanit API example:

    ```python
    from kyanitapi import Kyanit

    my_kyanit = Kyanit('BCG', network_addr='192.168.1.0')
    netvar = my_kyanit.netvar()  # netvar now equals to the value of Netvar.outbound()
    my_kyanit.netvar('some_value')  # 'some_value' will be sent to Kyanit, after which
                                    # Netvar.inbound() will return 'some_value'
    ```

    Setting and getting the netvar is realized through HTTP, so keep in mind that
    there's an order of a second time lag between every network operation. Netvar is not
    intended to be accessed continuously, because the network overhead would
    substantially slow down the operation of the Kyanit board.

    Instead use it for user commands, which depending on the project can be things like
    switching, reading sensor data, changing the LED colors, etc.
    """

    _in = None
    _out = None

    @staticmethod
    def inbound(obj=None, clear=False):
        """
        Get, set or clear the inbound variable.

        See class documentation for details.
        """

        if clear:
            Netvar._in = None
            return

        if obj is None:
            return Netvar._in

        Netvar._in = obj

    @staticmethod
    def outbound(obj=None, clear=False):
        """
        Get, set or clear the outbound variable.

        See class documentation for details.
        """

        if clear:
            Netvar._out = None
            return

        if obj is None:
            return Netvar._out

        Netvar._out = obj


def get_color_id():
    """
    Return the Color ID string of the Kyanit, which is derived from the current IP
    address.

    Returned value will be 'BBB' (address of 0) if Kyanit can not connect to the
    wireless network, or if it loses connection.
    """

    return _color_id


_controls_kyanit_leds = None
_controls_kyanit_button = None


def controls(
    kyanit_leds=None,
    kyanit_button=None,
    active_colors=((0, 50, 250),) * 3,
    idle_colors=((250, 50, 0),) * 3,
    brightness=1,
):
    """
    Optional decorator for `code.main` and `code.cleanup`.

    Having this decorator on `code.main` and `code.cleanup` gives visual feedback on run
    state, as well as showing the Color ID on the LEDs, when the button is pressed.

    When user code is running, the LEDs will continuously show the `active_colors` with
    a "breathing" animation. When code is stopped, the `idle_colors` will be shown with
    a slower "breathing" animation.

    Default colors may be changed by passing a list of 3 colors to `active_colors` and
    `idle_colors`. Each color must be an RGB tuple.

    On code error, the `idle_colors` will be shown, with an "attention" animation.

    `kyanit_leds` may be instance of `kyanit.neoleds.NeoLeds` to override default LEDs
    pin, and to provide additional custom functionality to the LEDs.

    `kyanit_button` may be instance of `kyanit.button.Button` to override default button
    pin. As of now, the button can not be used for any other functionality, if this
    decorator is used.

    The brightness of the LEDs can be adjusted with the `brightness` parameter, which
    must be a float between 0 (completely dark) and 1 (full brightness).
    """

    brightness = sorted((0, brightness, 1))[1]

    if kyanit_leds is None:
        from . import neoleds

        global _controls_kyanit_leds
        if _controls_kyanit_leds is None:
            _controls_kyanit_leds = neoleds.NeoLeds(LEDS_PIN, 3)
        kyanit_leds = _controls_kyanit_leds
    if kyanit_button is None:
        from . import button

        global _controls_kyanit_button
        if _controls_kyanit_button is None:
            _controls_kyanit_button = button.Button(BUTTON_PIN)
        kyanit_button = _controls_kyanit_button

    brightness = sorted([0, brightness, 1])[1]

    async def show_cid_on_leds():
        while True:
            if kyanit_button.check() == "click":
                kyanit_leds.display(colorid.to_colors(get_color_id()), time=10)
            await runner.sleep_ms(100)

    def decorator(func):
        # wrapper for code.main and code.cleanup
        def wrapper(*args):
            from .neoleds import Animations

            runner.create_task("kyanit_leds", kyanit_leds.refresh_leds)
            runner.create_task("kyanit_button", kyanit_button.monitor)
            runner.create_task("kyanit_show_cid", show_cid_on_leds)
            if not args:
                kyanit_leds.display(
                    active_colors,
                    Animations.breathe,
                    anim_speed=10,
                    brightness=brightness,
                )
            elif args[0] is StoppedError or args[0] is None:
                kyanit_leds.display(
                    idle_colors, Animations.breathe, anim_speed=5, brightness=brightness
                )
            elif args[0] is not RebootError:  # and args[0] is not ResetError:
                kyanit_leds.display(
                    idle_colors,
                    Animations.attention,
                    anim_speed=10,
                    brightness=brightness,
                )
            func(*args)

        return wrapper

    return decorator


def run():
    global _color_id

    PROTECTED_FILES = ["/main.py", "/boot.py", "/_boot.py"]

    class FileServerError(Exception):
        pass

    def setup_fallback_ap():
        unique_id = ubinascii.hexlify(machine.unique_id()).upper().decode()
        interfaces.ap.active(True)
        interfaces.ap.config(
            essid="Kyanit {}".format(unique_id),
            password="myKyanit",
            authmode=network.AUTH_WPA_WPA2_PSK,
        )

    async def leds_ap_mode(neop):
        # when fallback AP is active
        trigger = False
        while True:
            trigger = not trigger
            for idx in range(3):
                neop[idx] = (0, 0, 64) if idx == 0 and trigger else (0, 0, 0)
            neop.write()
            await runner.sleep_ms(250)

    async def check_wlan_connection():
        global _color_id

        while True:
            await runner.sleep(30)
            if not interfaces.wlan.isconnected():
                _color_id = "BBB"
            elif _color_id == "BBB":
                _color_id = colorid.from_number(
                    int(
                        ure.search("\d+$", interfaces.wlan.ifconfig()[0]).group(0)
                    )  # noqa
                )

    def action_file_list(*args):
        return httpsrv.response(
            200,
            ujson.dumps(
                [
                    path
                    for path in uos.listdir("/")
                    if "\x00" not in path  # ignore garbage files
                    and uos.stat(path)[0] == 32768  # noqa
                    and path not in PROTECTED_FILES  # noqa
                ]
            ),
            httpsrv.CT_JSON,
        )

    def action_files(method, loc, params, headers, conn, addr):
        if "/" in loc[7:]:  # only files in root dir are allowed
            raise FileServerError("not on root")

        file_name = loc[6:]

        if file_name in PROTECTED_FILES:
            raise FileServerError("restricted")

        try:
            stat = uos.stat(file_name)
        except OSError:
            if method == "GET" or method == "DELETE" or "rename" in params:
                return httpsrv.response(404, '"File Not Found"', httpsrv.CT_JSON)
        else:
            if stat[0] != 32768:
                raise FileServerError("restricted")

        if method == "DELETE":
            uos.remove(file_name)
            return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

        if method == "GET":
            with open(file_name, "rb") as file:
                # read from file, send to conn
                httpsrv.send_response(
                    conn, **(httpsrv.response(200, content_type=httpsrv.CT_PLAIN))
                )
                httpsrv.readall_from(file, into=conn)
            return None  # response already assembled above

        elif method == "PUT":
            if "rename" in params:
                uos.rename(file_name, params["rename"])
                return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

            with open(file_name, "wb") as file:
                # write to file, receive from conn
                httpsrv.readall_from(conn, into=file)
            return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

    async def reboot():
        await runner.sleep(1)
        print("KYANIT Hard Reset!")
        machine.reset()

    def action_reboot(method, loc, params, headers, conn, addr):
        runner.stop(exc=RebootError)
        runner.get_event_loop().create_task(reboot())
        return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

    def action_state(method, loc, params, headers, conn, addr):
        return httpsrv.response(
            200,
            ujson.dumps(
                {
                    "unique_id": ubinascii.hexlify(
                        machine.unique_id()
                    ).decode().upper(),
                    "micropython_version": uos.uname().version[
                        1:uos.uname().version.index(" ")
                    ],
                    "firmware_version": __version__,
                    "color_id": _color_id,
                    "free_memory": gc.mem_free(),
                    "free_flash": uos.statvfs("/")[0] * uos.statvfs("/")[3],
                    "run_state": [
                        "ERROR {}".format(runner.get_error()[0])
                        if runner.get_error() is not None
                        else "",
                        "STOPPED",
                        "CODE.PY MISSING",
                        "CODE.PY IMPORTED",
                        "CODE.PY MAIN",
                    ][runner.get_state()],
                    "error_traceback": [
                        line.strip()
                        for line in runner.get_error()[1].split("\n")
                        if line and "Traceback" not in line
                    ]
                    if runner.get_error() is not None
                    else None,  # noqa
                }
            ),
            httpsrv.CT_JSON,
        )

    def action_runner_start(method, loc, params, headers, conn, addr):
        runner.start()
        return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

    def action_runner_stop(method, loc, params, headers, conn, addr):
        runner.stop(force=True if "force" in loc else False, exc=StoppedError)
        return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)

    def action_netvar(method, loc, params, headers, conn, addr):
        if method == "POST":
            Netvar.inbound(ujson.loads(httpsrv.readall_from(conn).getvalue().decode()))
            return httpsrv.response(200, '"OK"', httpsrv.CT_JSON)
        if method == "GET":
            return httpsrv.response(
                200, ujson.dumps(Netvar.outbound()), httpsrv.CT_JSON
            )

    # Start in fallback AP mode if the button is pressed
    fallback_ap_mode = False
    button = machine.Signal(machine.Pin(BUTTON_PIN, machine.Pin.IN), invert=True)
    if button.value():
        fallback_ap_mode = True

    # Try connecting to WLAN if not in fallback AP, else activate AP
    if not fallback_ap_mode:
        try:
            wlan_info = ujson.load(open("/wlan.json"))
            ssid = wlan_info["ssid"]
            password = wlan_info["password"]
            ifconfig = wlan_info["ifconfig"] if "ifconfig" in wlan_info else "dhcp"
        except Exception:
            # fall back to AP, if can't get JSON, or malformed
            fallback_ap_mode = True
            setup_fallback_ap()
        else:
            if not interfaces.wlan_connect(
                ssid, password, ifconfig=ifconfig, timeout=20
            ):
                # fall back to AP, if can't connect
                interfaces.wlan.active(False)
                fallback_ap_mode = True
                setup_fallback_ap()
    else:
        fallback_ap_mode = True
        setup_fallback_ap()

    # Show fallback AP mode on LEDs
    if fallback_ap_mode:
        neop = neopixel.NeoPixel(machine.Pin(LEDS_PIN), 3)
        loop = runner.get_event_loop()
        loop.create_task(leds_ap_mode(neop))

    # Set Color ID
    _color_id = colorid.from_number(
        int(ure.search("\d+$", interfaces.wlan.ifconfig()[0]).group(0))  # noqa
    )

    # Set up HTTP server
    http_server = httpsrv.HTTPServer(port=3300)

    # File actions
    http_server.register("GET", "^/files$", action_file_list)
    http_server.register("GET", "^/files/$", action_file_list)
    http_server.register("GET", "^/files/.*", action_files)
    http_server.register("PUT", "^/files/.*", action_files)
    http_server.register("DELETE", "^/files/.*", action_files)

    # System actions
    http_server.register("GET", "^/sys/state$", action_state)
    http_server.register("POST", "^/sys/reboot$", action_reboot)
    http_server.register("POST", "^/sys/reboot/soft$", action_reboot)

    # Runner actions
    http_server.register("POST", "^/sys/start$", action_runner_start)
    http_server.register("POST", "^/sys/stop$", action_runner_stop)
    http_server.register("POST", "^/sys/stop/force$", action_runner_stop)

    # Netvar actions
    http_server.register("GET", "^/netvar$", action_netvar)
    http_server.register("POST", "^/netvar$", action_netvar)

    # RUN
    loop = runner.get_event_loop()
    loop.create_task(http_server.catch_requests())

    if not fallback_ap_mode:
        # start code.py if not in fallback AP mode
        loop.create_task(check_wlan_connection())
        loop.create_task(runner.starter_coro())

    try:
        loop.run_forever()
    except Exception:
        # close socket, so we can restart
        http_server.close()
        raise
