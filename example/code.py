# This code is imported on startup, then main is called, if it exists. Neither main, nor
# cleanup should block for too long.
# Use coroutines through kyanit.runner.create_task('name', coro) for continuous or
# longer tasks. Any errors (including from coroutines) will be passed to cleanup.
# The @kyanit.controls() decorator adds functionality to the LEDs and button. It can be
# removed if this is not needed, to save approximately 1k of RAM.

# To get started, head to https://kyanit.eu

import kyanit


@kyanit.controls()
def main():
    pass


@kyanit.controls()
def cleanup(exception):
    pass
