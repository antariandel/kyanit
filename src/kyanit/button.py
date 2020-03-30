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


import utime
import uasyncio
import machine


class Button:

    def __init__(self, pin_number, invert=True):
        self._button_signal = machine.Signal(machine.Pin(pin_number, machine.Pin.IN),
                                             invert=invert)

        self._last_button_press = (None, None)
        self._last_known_button_press = (None, None)

    async def monitor(self):
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
        if self._last_known_button_press != self._last_button_press:
            self._last_known_button_press = self._last_button_press
            return self._last_button_press[0]
        
        return None
