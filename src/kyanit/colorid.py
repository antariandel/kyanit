# Kyanit (Core) - colorid module
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
# `kyanit.colorid` module

This module publishes two helper functions to work with Color IDs.

See the function documentations for details on usage.
"""


_valid_id_colors = {
    "B": (0, 0, 255),
    "C": (0, 128, 128),
    "G": (0, 128, 0),  # brightness compensated
    "M": (128, 0, 128),
    "R": (128, 0, 0),  # brightness compensated
    "W": (85, 85, 85),
    "Y": (128, 128, 0),
}


def to_colors(color_id):
    """
    Return a list with 3 RGB color tuples corresponding to the `color_id`. The
    `color_id` must be a string with 3 upper-case characters, which can be any of 'R',
    'G', 'B', 'C', 'M', 'Y', or 'W' (white).

    If the `color_id` is a longer string, subsequent characters are disregarded. If the
    first 3 characters are not one of the above list, `IndexError` will be raised.

    `color_id` may also be any other indexable type, but if `color_id` is not indexable,
    `TypeError` will be raised.
    """

    return [
        _valid_id_colors[color_id[0]],
        _valid_id_colors[color_id[1]],
        _valid_id_colors[color_id[2]],
    ]


def from_number(num):
    """
    Calculate a Color ID string from a number passed to `num`. If `num` is negative or
    larger than 342, `ValueError` will be raised. The Color ID is used for representing
    the last octet of an IP address, so any value above 245 is probably also not valid,
    but 342 is the maximum number that can be represented with the 7 available color
    symbols.

    If `num` is not `int`, `TypeError` will be raised.
    """

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

    result = "".join(digits)

    return (symbols[0] * (3 - len(result))) + result  # pad
