# Kyanit (Core) - utils module
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


_valid_id_colors = {
    'B': (0, 0, 255),
    'C': (0, 128, 128),
    'G': (0, 128, 0),  # brightness compensated
    'M': (128, 0, 128),
    'R': (128, 0, 0),  # brightness compensated
    'W': (85, 85, 85),
    'Y': (128, 128, 0)
}


def id_to_colors(color_id):
    return [
        _valid_id_colors[color_id[0]],
        _valid_id_colors[color_id[1]],
        _valid_id_colors[color_id[2]],
    ]


def id_from_number(num):
    max_addr = len(_valid_id_colors) ** 3 - 1

    if num < 0 or num > max_addr:
        raise ValueError

    base = len(_valid_id_colors)
    symbols = [key for key in _valid_id_colors]
    symbols.sort()

    digits = []

    while num:
        digits.append(symbols[int(num % base)])
        num = int(num / base)

    digits.reverse()

    result = ''.join(digits)

    return (symbols[0] * (3 - len(result))) + result  # pad
