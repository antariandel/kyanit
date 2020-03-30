# Kyanit (Core) - neoleds module
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


import math
import utime
import machine
import uasyncio
import neopixel


class NeoLeds:
    def __init__(self, pin_number, num_leds):
        self._num_leds = num_leds
        self._leds_pin = machine.Pin(pin_number)
        self._neopixel = neopixel.NeoPixel(self._leds_pin, num_leds)
        
        # clear the neopixels:
        self._write_colors([(0, 0, 0)] * self._num_leds)
        
        self._colors = [None, None]  # [0] is indef. [1] is temp.
        self._anim = [None, None]  # same as above
        self._anim_speed = [None, None]  # same as above
        self._anim_phase = 0
        self._temp_until = None

    def display(self, colors, anim=None, anim_speed=None, time=None):
        self._anim_phase = 0
        self._anim_speed[0 if time is None else 1] = sorted((1, anim_speed, 10))[1] \
                                                     if anim_speed is not None else None  # noqa
        self._colors[0 if time is None else 1] = colors
        self._anim[0 if time is None else 1] = anim
        self._temp_until = None if time is None else \
                           utime.ticks_add(utime.ticks_ms(), time * 1000)  # noqa

    async def refresh_leds(self):
        disp = 0

        while True:
            self._anim_phase += 1
            if self._anim_phase > 1000:
                self._anim_phase = 0
            if self._temp_until is not None:
                disp = 1  # temporary display
                if utime.ticks_ms() > self._temp_until:
                    self._temp_until = None  # check if temporary is over
            else:
                disp = 0  # indefinite display
            
            if self._colors[disp] is not None:
                self._write_colors(self._colors[disp] if self._anim[disp] is None else
                                   # call anim with the phase and colors
                                   self._anim[disp](self._anim_phase,
                                                    self._colors[disp]))

            # sleep between 0 and 9 ms based on _anim_speed
            await uasyncio.sleep_ms(10 - self._anim_speed[disp]
                                    if self._anim_speed[disp] is not None else 10)

    def _write_colors(self, colors=None):
        for color in enumerate(colors):
            self._neopixel[color[0]] = color[1]
        self._neopixel.write()


class Animations:

    @staticmethod
    def breathe(phase, colors):
        phase = phase % 500  # double the period
        return [tuple(
                    int(abs(
                        color_element / (2 + math.sin(math.pi * 2 * phase / 500))
                    )) for color_element in color
                ) for color in colors]  # noqa
    
    @staticmethod
    def attention(phase, colors):
        phase = phase % 333  # triple the period
        
        def anim(x):
            if x < 167:
                return 11 - 10 * x / 167
            elif x < 200:
                return 1
            elif x < 217:
                return 5
            elif x < 233:
                return 1
            elif x < 250:
                return 5
            elif x < 267:
                return 1
            else:
                return 11

        return [tuple(
                    int(abs(
                        color_element / anim(phase)
                    )) for color_element in color
                ) for color in colors]  # noqa
