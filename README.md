# __Kyanit__ Core Module

## Introduction

Kyanit is a user code supervisor built for MicroPython. Development is currently focused on the
ESP8266 port of MicroPython. Together with an ESP8266 board, Kyanit is indended to be a foundation
for home automation systems. An official board design for Kyanit can be found at
https://kyanit.eu/kyanit-board

For information about MicroPython head to https://github.com/micropython/micropython

Being a supervisor, Kyanit is responsible for starting and stopping user code, as well as handling
any uncaught exceptions in the user code.

Kyanit provides an HTTP API through which the user code can be changed and controlled. Additionally
it provides an addressing mechanism called the "Color ID," which mapps to the IP address of the
board. The Color ID consists of 3 colors from the **R**ed, **G**reen, **B**lue, **C**yan,
**M**agenta, **Y**ellow and **W**hite pallette, and is displayed using 3 WS2812B (Neopixel) LEDs.

The official board design already has these LEDs built in, as well as a button, which when pressed,
will display the Color ID on the LEDs.

## The Kyanit Ecosystem

* [**Kyanit Core**](https://github.com/kyanit-project/kyanit)

This repo. The core Kyanit module, flashed into an ESP8266 board.

* [**Kyanit Board**](https://github.com/kyanit-project/kyanit-board)

A stylish, triangle-shaped ESP8266-base board built around an ESP-12F module, the official Kyanit
controller board.

* [**Kyanit CTL**](https://github.com/kyanit-project/kyanitctl)

Command-line utility for interacting with Kyanit.

* [**Kyanit API**](https://github.com/kyanit-project/kyanitapi)

Python API for interaction with Kyanit from Python code. (It is used by Kyanit CTL.)

## Getting Started with Kyanit

### Setting Up

The core module is intended to be compiled into the MicroPython firmware, and flashed into an
ESP8266. A board with at least 1 MB of flash is recommended, leaving approximately 380 kB free for
user code. The Kyanit Board, or any other board with an ESP-12E/F is a good candidate. If you will
not be using the Kyanit Board, wire 3 WS2812B LEDs to Pin(4), and an active-low button to Pin(14).
If you're new to the WS2812B LEDs, you can refer to this extensive tutorial on SparkFun:
https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all

NOTE: It is possible to use the core module without flashing it into the firmware, but substantially
less RAM will be available (~5k versus ~20k).

To flash a released version, see the
[*Flashing a Released version of Kyanit*](#flashing-a-released-version-of-kyanit) section further
below. Alternatively you can build the current development version, in that case, see
[*Building from Source (Linux)*](#building-from-source-linux).

The first time you power up the board, it will set up an AP with an SSID starging with `Kyanit` and
ending with a 4-digit hex number derived from the flash ID. (NOTE: It is not intended to be globally
unique, insted it provides an easy way to differentiate a handful of them.)
When the AP is active, the LEDs will flash blue.

A command-line utility called `kyanitctl` is provided for managing a Kyanit board.
To start interacting with the board, install it from PyPI with:

```
pip install kyanitctl
```

Connect to Kyanit's SSID, then start setting up Kyanit to connect to your home WiFi using DHCP with:

```
kyanitctl -setup
```

Follow the instructions and enter your home network SSID and password. You can then review your
settings before it gets uploaded to the board. A mostly blank example `code.py` will be uploaded
along with the WiFi settings. This file is the user code startup file.

Alternatively you can set up a static IP by running the setup with:

```
kyanitctl -setupstatic
```

Choose an IP address that's outside of the DHCP pool of your router. If you're unsure, use `-setup`
instead.

Kyanit will then reboot and try to connect to your WiFi. If this doesn't work, it will fall back
to AP, and start flashing the LEDs again. You can retry the above steps, if this happens.

On successful connection, the LEDs will light up in a greenish-blue color, with a slow "breathing"
animation. If you were originally connected to your home network through WiFi, you can now
reconnect.

Pressing the button will cause the Color ID to be shown on the LEDs for 10 seconds. On a Kyanit
Board, the Color ID must be read starting from the bottom, and going clockwise. Here are some
examples:

--- INCLUDE IMAGE ---

Addressing using the Color ID works on home networks with a subnet mask of 255.255.255.0, which is
what most home and small business routers create. Kyanit CTL will discover the networks available
on your computer the first time you run it with a Color ID. If one such network is present on your
system, it will be used by default, otherwise you will be presented with a list of networks, and
you'll need to select the same network, Kyanit is connected to. The selection will be saved and
used for all further connection attempts. (Network selection can be re-run with
`kyanitctl -reset_network`.)

Try running `kyanitctl <colors> -status` (or `-stat` for short) to see the current status of the
board.

Here's an example output for a Kyanit Board with a Color ID of BBY (Blue-Blue-Yellow) on a system
where two networks with a netmask of 255.255.255.0 are present:

```
> kyanitctl BBY -stat

=== Network Setup ===

Connecting to Kyanit with the Color ID works on networks with a netmask of 255.255.255.0 (most home 
wireless networks). Multiple such networks detected. Select the one Kyanit is connected to:

0: 192.168.137.0   Ethernet
1: 192.168.1.0     Wi-Fi

Select network [0, 1]: 1
Saved. You may re-run this setup with -reset_network.

=== Kyanit BBY (192.168.1.6 through 'Wi-Fi') ===

Retrieving system status...

    Firmware version: 0.1.0
          Free flash: 3514368
         Free memory: 15776
           Run state: CODE.PY MAIN

```

Having the network saved, further runs will provide a much concise output:

```
=== Kyanit BBY (192.168.1.6 through 'Wi-Fi') ===

Retrieving system status...

    Firmware version: 0.1.0
          Free flash: 3514368
         Free memory: 18800
           Run state: CODE.PY MAIN
```

The IP address that the Color ID maps to will be displayed.

In the unlikely scenario where your home WiFi is configured with a netmask different from
255.255.255.0, you'll need to provide the IP address of the Kyanit when running `kyanitctl`. In this
case it's easier if Kyanit is configured with a static IP.

The same as above with IP address would be:

```
kyanitctl -ip 192.168.1.6 -stat

...
```

### Downloading and Uploading Files

List the files currently on the board with the `-files` option:

```
> kyanitctl BBY -files

=== Kyanit BBY (192.168.1.6 through 'Wi-Fi') ===

Retrieving file list done. Files:

wlan.json
code.py

```

With a fresh install, you should see `wlan.json` with your WiFi credentials and IP settings, and
`code.py`, which is the user code.

Download `code.py` from the board with `-get code.py`. (Be aware, that this will overwrite any
existing `code.py` that you may have in the local directory.)

The `code.py` initially contains the following:

```python
# This code is imported on startup, then main is called, if it exists. Neither main, nor cleanup
# should block for too long. Use coroutines through kyanit.runner.create_task('name', coro) for
# continuous or longer tasks. Any errors (including from coroutines) will be passed to cleanup.
# The @kyanit.controls() decorator adds functionality to the LEDs and button. It can be removed if
# this is not required, to save ~1k of RAM.

# To get started, read more at https://kyanit.eu


import kyanit


@kyanit.controls()
def main():
    # Put startup code here.
    pass


@kyanit.controls()
def cleanup(exception):
    # Put error-handling code here, as well as code that needs to be run when stopped, or
    # before reboot.
    pass
```

Uploading a new `code.py` can be done with `-put code.py`. Other files can also be uploaded.
If you pass a directory to `-put`, every file from that directory will be uploaded (it will not
recurse, as directories are not supported by Kyanit).

NOTE: The board will need to be rebooted with `-reboot` for the new code to become active. This can
be done with a single command, for example:

```
kyanitctl BBY -put code.py -reboot
```

For a full list of what Kyanit CTL can do, refer to the command-line help with `kyanitctl -h`.

### Run States

There are 5 different run states: `CODE.PY MISSING`, `CODE.PY IMPORTED`, `CODE.PY MAIN`, `STOPPED`
and `ERROR`.

* **`CODE.PY MISSING`**

There's no `code.py` file to import and run.

* **`CODE.PY IMPORTED`**

There is a `code.py`, that was imported, but there's no `main` function to call.

* **`CODE.PY MAIN`**

`code.py` was imported, and `main` was called. This is what can be considred a "running" state.

* **`STOPPED`**

The code was stopped either from within the code itself, or by outside means, ex. with Kyanit CTL's
`-stop` option. The code may be restarted with Kyanit CTL, using the `-start` option.

* **`ERROR ExceptionName`**

There was an uncaught exception within `code.py`. An exception detail, with traceback will also be
available through Kyanit CTL's `-status` option. At this point, the code may be restarted.
(Although debugging is probably required.)

## Coding on Kyanit (Using Coroutines)

Kyanit is built around MicroPython's uasyncio. (CPython's asyncio implementation for MicroPython.)
This means Kyanit is all about coroutines. Albeit it's advisable to learn about coroutines before
coding on Kyanit, it's not entirely required, if you abide by some basic rules.

A coroutine is just a function defined with `async`:

```python
async def myfunc():
    # This is a coroutine
    pass
```

Coroutines are not multithreaded, but they can be understood as if they were running alongside each
other in parallel.

Every internal functionality of Kyanit is built using coroutines. This means, that your code in
`code.py` must also use coroutines to achieve continuous functionality. Nothing within `code.py`
should block for too long, because this essentially freezes the whole system, preventing Kyanit from
running its internal tasks, rendering it unresponsive.

In short, this means no continuous loops (with `while True`) within any non-async functions, which
includes `main` and `cleanup`.

`main` is intended to set up your own code and potentially start coroutines, which will run
alongside Kyanit's internal tasks.

Likewise, `cleanup` is intended to run quickly after some exception, potentially acting on them.

`cleanup` is also called when code is stopped or rebooted, with `kyanit.StoppedError` and
`kyanit.RebootError` passed respectively. This lets you do stuff on these two events, if desired.

Here's a simple example of a continuosly running task in `code.py`:

```python
from kyanit import controls, runner


async def my_task():
    while True:
        # do some stuff
        await runner.sleep(1)


@controls()
def main():
    runner.create_taks('my_task_name', my_task)


@controls()
def cleanup(exception):
    pass
```

The above code will immediately start `my_task`. Note the `await` statement, which will give CPU
time for other coroutines to run. In this case, the uasyncio scheduler will return to `my_task`
after 1 second. You must have an `await` statement inside your coroutines to yield CPU time to other
tasks. You may also `await` other coroutines that you defined.

**You may await a sleep time of 0**, which basically means "return to this function as soon as
possible." The scheduler will give time to other tasks that are not awaiting a sleep, and will
return to the function as soon as those tasks arrive to an `await` statement.

HINT: Everything from uasyncio is available in `runner` (it has `from uasyncio import *`).

### About `runner.create_task()`

Always create tasks with `runner.create_task()` and not `uasyncio.get_event_loop().create_task()`,
because Kyanit can not catch errors in tasks created on the event loop directly. Uncaught errors
will cause the coroutine that's raising them to stop silently, which may result in unexpected
behavior.

On the other hand, errors in tasks created on runner will be handled. In case of errors, tasks will
be stopped in a controlled fashion.

The same applies when running is stopped with `kyanit.runner.stop()` or by ex. Kyanit CTL, using
`-stop`. Kyanit will stop all tasks created on runner, but it will not stop tasks directly created
on the event loop.

Stop tasks from running with `runner.destroy_task('task_name')`.

### The things to keep in mind:
* If you want a long-running loop, implement it in an `async` function
* Never use `time.sleep()` for long delays, use `await runner.sleep()` instead
* If timing is critical (ex. for bit-banging), you may use `time.sleep()`, but keep in mind that
this prevents other coroutines to run in the meantime, so keep it short.
* Always create tasks with `runner.create_task()`

More on coroutines in MicroPython:
https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md

NOTE: `micropython/extmod/uasyncio` (the one available in Kyanit) is a different implementation,
than what the above tutorial is based on, but it's still a good place to start. See source
`uasyncio` code at https://github.com/micropython/micropython/tree/master/extmod/uasyncio to find

out differences.

## Flashing a Released version of Kyanit

Download the latest version from releases, then refer to MicroPython documentation on flashing
frimware onto an ESP8266 here: https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

## Building from Source (Linux)

Building from source will require the ESP Open SDK. You can find it here:
https://github.com/pfalcon/esp-open-sdk

Clone the repository and build the SDK per instructions in the repo.

After building the SDK, clone the MicroPython repository from
https://github.com/micropython/micropython, then go into `micropython/mpy-cross` and build
`mpy-cross` with `make`.

WebREPL is not included in Kyanit, because it's intended to be always running, and never exiting
to REPL. Therefore, to save flash, remove WebREPL from the build by commenting out these lines in
`micropython/ports/esp8266/mpconfigport.h` (around line 85):

```
//#define MICROPY_PY_WEBREPL                (1)
//#define MICROPY_PY_WEBREPL_DELAY          (20)
//#define MICROPY_PY_WEBREPL_STATIC_FILEBUF (1)
```

(NOTE: Even if you do not comment these lines out, WebREPL will not be available, as it's not
included in the board's manifest. You need to add them there, if you want WebREPL.)

Make a custom board configuration by copying `micropython/ports/esp8266/boards/GENERIC` to
`[...]/boards/KYANIT`.

Copy the `micropython/ports/esp8266/modules` directory to
`KYANIT/modules`, then copy the contents of `kyanit/src` into the newly created `modules` directory.

Copy `kyanit/mpbuild/manifest.py` to the `KYANIT` directory, overwriting the existing file.

Additionally delete the `inisetup.py` file from `modules`, as it's not needed for Kyanit.

After these operations, the `KYANIT` directory should look like this:

```
boards/KYANIT
├── manifest.py         (from kyanit/mpbuild)
├── modules
│   ├── _boot.py
│   ├── apa102.py
│   ├── boot.py         (from kyanit/src)
│   ├── flashbdev.py
│   ├── ...             (inisetup.py deleted)
│   ├── kyanit          (from kyanit/src)
│   │   └── ...
│   ├── main.py         (from kyanit/src)
│   ├── neopixel.py
│   ├── ntptime.py
│   └── port_diag.py
├── mpconfigboard.h
└── mpconfigboard.mk
```

The board configuration is now ready for building. Inside `micropython/ports/esp8266/`, build it
with:

```
make BOARD=KYANIT
```

The resulting firmware file will be `micropython/ports/esp8266/build-KYANIT/firmware-combined.bin`.

For flashing the firmware onto an ESP8266, you'll need `esptool`. Install it with:

```
pip install esptool
```

Having `esptool` installed, flash the firmware with:

```
make deploy BOARD=KYANIT PORT=<your serial port>
```

(You can play with baudrates for faster flashing, ex. appending `BAUD=230400` to the deploy
command.)

## Thank-yous

Special thanks to the MicroPython community and Damien George. And thanks for being so responsive
on issues.

## License Notice

Copyright (C) 2020 Zsolt Nagy

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.
