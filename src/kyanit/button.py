# Kyanit (Core) - button module
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

"""
# `kyanit.button` module

This module publishes the `Button` class, which can be used to monitor a button and catch button
press events.

Here"s a simple example in `code.py`, that will do something on button press on Pin(5):

```python
import kyanit
from kyanit import runner
from kyanit.button import Button

async def do_something_on_click(button):
    while True:
        if button.check() == 'click':
            # do something on button press here
            ...
        await runner.sleep_ms(100)

@kyanit.controls()
def main():
    my_button = Button(5, True)  # active-low button on Pin(5)
    runner.create_task('my_button_monitor', my_button.monitor)  # start monitoring task
    runner.create_task('on_click', do_something_on_click, my_button)

@kyanit.controls(brightness=0.1)
def cleanup(exception):
    pass
```

See the `Button` class documentation for details on usage.
"""


import utime
import uasyncio
import machine


class Button:
    """
    Instantiate this class with a pin number to catch button-press events on the pin. The pin number
    is the GPIO number on the controller.

    If the button is active-high (ie. it's logical high on press, and logical low by default), set
    `invert` to `False`.

    Once instantiated, the `monitor` task must be started for button monitorization. After that,
    check the last button press event with the `check` function.

    NOTE: You should check button events frequently, because if more than 1 event occurs between
    checks, only the last event will be returned. Frequent checks will also make the button more
    responsive. A 100ms wait between checks should be a good choice.
    """

    def __init__(self, pin_number, invert=True):
        self._button_signal = machine.Signal(machine.Pin(pin_number, machine.Pin.IN),
                                             invert=invert)

        self._last_button_press = (None, None)
        self._last_known_button_press = (None, None)

    async def monitor(self):
        """
        This task continuously monitors the button. It must be started for `check` to work.
        """
        # TODO: Make more sophisticated (pattern based)

        while True:
            if self._button_signal.value():
                await uasyncio.sleep_ms(50)
                if self._button_signal.value():
                    await uasyncio.sleep_ms(250)
                    if self._button_signal.value():
                        await uasyncio.sleep(3)
                        if self._button_signal.value():
                            self._last_button_press = ('long3s', utime.ticks_ms())
                            while self._button_signal.value():
                                await uasyncio.sleep_ms(500)
                        else:
                            self._last_button_press = (None, utime.ticks_ms())
                    else:
                        self._last_button_press = ('click', utime.ticks_ms())

            await uasyncio.sleep(0)

    def check(self):
        """
        Return the last new event on the button.

        Supported events:

        * `'click'` (the button was pressed for shorter than 250ms)
        * `'long3s'` (the button was pressed for at least 3 seconds)

        Return value will be one of the supported event names.
        """
        if self._last_known_button_press != self._last_button_press:
            self._last_known_button_press = self._last_button_press
            return self._last_button_press[0]
        
        return None
