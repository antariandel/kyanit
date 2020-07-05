# Kyanit (Core) - runner module
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


import sys

import uio
import uos
from uasyncio import *  # noqa

_loop = get_event_loop()
_tasks = {}

_error_name = ""
_traceback = ""


ERROR = 0
STOPPED = 1
CODE_MISSING = 2
CODE_IMPORTED = 3
CODE_MAIN = 4


_state = STOPPED


def get_state():
    return _state


def get_error():
    return (_error_name, _traceback) if _state == ERROR else None


def get_tasks():
    return _tasks


def start():
    global _state

    if _state <= STOPPED:
        try:
            uos.stat("/code.py")

        except Exception:
            _state = CODE_MISSING
            return

        try:
            import code

            _state = CODE_IMPORTED
            if hasattr(code, "main"):
                if callable(code.main):
                    code.main()
                    _state = CODE_MAIN

        except ImportError as exc:
            _handle_error(exc, cleanup=False)

        except Exception as exc:
            _handle_error(exc, cleanup=True)


async def starter_coro():
    start()


def stop(force=False, exc=None):
    global _state

    if _state > STOPPED or force:
        for task_name in _tasks:
            destroy_task(task_name)
        _state = STOPPED

        if not force:
            try:
                import code

                if hasattr(code, "cleanup"):
                    # pass exc to cleanup
                    code.cleanup(exc)

            except Exception as exc:
                _handle_error(exc, False)


async def stopper_coro():
    stop()


def create_task(name, coro, *args):
    if str(name) not in _tasks:
        try:
            _tasks[name] = _loop.create_task(_task_wrapper_coro(coro, *args))
        except Exception as exc:
            _handle_error(exc, True)
        else:
            return True

    return False


def destroy_task(name):
    if str(name) in _tasks:
        try:
            _tasks[name].cancel()
        except RuntimeError:
            # coroutine is executing (cannot cancel self)
            pass
        del _tasks[name]
        return True

    return False


async def _task_wrapper_coro(coro, *args):
    try:
        await coro(*args)

    except CancelledError:
        pass  # allow cancellation silently (ie. when deactivating)

    except Exception as exc:
        _handle_error(exc, True)


def _handle_error(exc, cleanup):
    global _state, _error_name, _traceback

    stop(force=True)
    _state = ERROR
    _error_name = exc.__class__.__name__

    exc_details = uio.StringIO()
    sys.print_exception(exc, exc_details)
    _traceback = exc_details.getvalue()

    if cleanup:
        try:
            import code

            if hasattr(code, "cleanup"):
                code.cleanup(exc)

        except Exception as exc:
            exc_details = uio.StringIO()
            sys.print_exception(exc, exc_details)
            _traceback = "{0}\nCODE.CLEANUP ERROR\n{1}".format(
                _traceback, exc_details.getvalue()
            )
