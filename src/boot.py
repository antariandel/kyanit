# Kyanit (Core) - boot.py
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


try:
    import kyanit
    if hasattr(kyanit, '__version__'):
        print('KYANIT {}'.format(kyanit.__version__))
except ImportError:
    print('KYANIT Error: Importing Kyanit FAIL!')
else:
    try:
        kyanit._run()
    except KeyboardInterrupt:
        print('KYANIT Stopping... Please wait.')
        kyanit.runner.stop()
        print('KYANIT Killed. Start again with kyanit._run()')
    except Exception as exc:
        # we should never end up here
        print('KYANIT Error: Unhandled Exception!')
        kyanit.runner.stop()
        raise exc