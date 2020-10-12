# Kyanit (Core) - _boot.py
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


import gc

import esp
import uos
import machine
from flashbdev import bdev

esp.osdebug(None)
gc.threshold((gc.mem_free() + gc.mem_alloc()) // 4)

if bdev:
    try:
        uos.mount(bdev, "/")

    except Exception:
        uos.VfsLfs2.mkfs(bdev)
        vfs = uos.VfsLfs2(bdev)
        uos.mount(vfs, "/")

gc.collect()

machine.freq(160000000)
