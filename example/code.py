# This code is imported on startup, then main is called, if it exists. Neither main, nor cleanup
# should block for too long. Use coroutines through kyanit.runner.create_task('name', coro) for
# continuous or longer tasks. Any errors (including from coroutines) will be passed to cleanup.
# The @kyanit.controls() decorator adds functionality to the LEDs and button. It can be removed if
# this is not required, to save approximately 1k of RAM.

# To get started, head to https://kyanit.eu


from kyanit import neoleds, controls, runner

leds = neoleds.NeoLeds(13, 48)


def blend_colors(color, blend_color, factor):
    def _mul_list_int(lst, val):
        return [int(item * val) for item in lst]

    def _add_lists(lst1, lst2, sign=1):
        return [item1 + sign * item2 for item1, item2 in zip(lst1, lst2)]
    
    return _add_lists(
        color,
        _mul_list_int(
            _add_lists(
                blend_color,
                color,
                -1
            ),
            factor
        )
    )


def rotate_anim(steps=100, direction=1):
    steps = sorted([0, steps, 999])[1]
    dr = 1 if direction > 0 else -1

    def animation(phase, colors):
        phase = phase % steps  # phase within one complete rotation
        num_leds = len(colors)  # number of leds
        color_period = steps / num_leds  # period of one pixel transition
        color_idx = int(phase / color_period)  # index of first color as it rotates
        blend = (phase % color_period) / color_period  # blend factor while transitioning

        return [blend_colors(colors[(idx + color_idx * dr) % num_leds],
                             colors[(idx + (color_idx + 1) * dr) % num_leds],
                             blend) for idx, color in enumerate(colors)]

    return animation


def simple_gradient(start_color, end_color, length):
    blend = 1 / length
    return [blend_colors(start_color, end_color, blend * i) for i in range(length)]


def gradient(colors, stops):
    stops = sorted(stops)
    grad_out = []
    for idx, stop in enumerate(stops):
        c_idx = idx + 1
        grad_out.extend(
            simple_gradient(colors[c_idx - 1], colors[c_idx],
                            stop - (stops[idx - 1] - 1 if idx > 0 else 0)))
        last_color = grad_out.pop()
    grad_out.append(last_color)
    
    return grad_out


def even_gradient(colors, length, circular=False):
    if circular:
        colors.append(colors[0])
    num_segments = len(colors) - 1
    seg_length = length / num_segments
    stops = [int(seg_length * (i + 1)) for i in range(num_segments)]
    stops[-1] = length
    print(stops)
    return gradient(colors, stops)


animator = rotate_anim()


def duplicate(phase, colors):
    colors = animator(phase, colors)
    colors.extend(reversed(colors))
    return colors


async def start_rotate_anim():
    leds.display(even_gradient([(150, 0, 200),
                                (0, 200, 0),
                                (0, 0, 255),
                                (255, 0, 0),
                                (255, 255, 0),
                                (0, 255, 0)], 24, circular=True), duplicate)


@controls()
def main():
    runner.create_task('refresher', leds.refresh_leds)
    # runner.create_task('rotater', start_rotate_anim)


@controls()
def cleanup(exception):
    pass
