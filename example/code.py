# This code is imported on startup, then main is called, if it exists. Neither main, nor cleanup
# should block for too long. Use coroutines through kyanit.runner.create_task('name', coro) for
# continuous or longer tasks. Any errors (including from coroutines) will be passed to cleanup.
# The @kyanit_controls() decorator adds functionality to the LEDs and button. It can be removed if
# this is not required, to save approximately 1k of RAM.

# To get started, read more at https://kyanit.eu


from kyanit import kyanit_controls


@kyanit_controls()
def main():
    pass


@kyanit_controls()
def cleanup(exception):
    pass
