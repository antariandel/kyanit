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

* [**Kyanit CTL**](https://github.com/kyanit-project/kyanit-ctl)

Command-line utility for interacting with Kyanit.

* [**Kyanit API**](https://github.com/kyanit-project/kyanit-api)

Python API for interaction with Kyanit from Python code. (It is used by Kyanit CTL.)

## Documentation

Kyanit Core documentation is at https://kyanit.eu/docs/kyanit.

## Flashing a Released version of Kyanit

Download the latest `kyanit-core-<version>.bin` from
https://github.com/kyanit-project/kyanit/releases/latest, then refer to MicroPython documentation
on flashing firmware onto an ESP8266 here:
https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

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

**This is optional: Until a more automated build process is made, create a `_version.py` file inside
`kyanit/src/kyanit` with this content:**

```python
__version__ = '<latest_version>'
```

Where `<latest_version>` should be the output of `python genversion.py` with `-dev` appended, for
example: `1.0.0-dev` (to differentiate it form released versions). Again, this is optional.

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
