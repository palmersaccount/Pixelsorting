from colorsys import rgb_to_hsv

from util import *

# SORTING PIXELS #
lightness = lambda p: rgb_to_hsv(p[0], p[1], p[2])[2] / 255.0
intensity = lambda p: p[0] + p[1] + p[2]
hue = lambda p: rgb_to_hsv(p[0], p[1], p[2])[0] / 255.0
saturation = lambda p: rgb_to_hsv(p[0], p[1], p[2])[1] / 255.0
minimum = lambda p: min(p[0], p[1], p[2])


def PixelAppend(size1, size0, data, msg):
    r"""
    Making a 3D array of pixel values from a PIL image.
    -----
    :param size1: img.size[1]/height
    :param size0: img.size[0]/width
    :param data: PixelAccess object from img.load()
    :param msg: Message for the progress bar
    :returns: 3D array of pixel values.

    Example
    -----
    >>> pixels = PixelAppend(size1, size0, data, "Appending")
    """
    pixels = []
    for y in ProgressBars(size1, msg):
        Append(pixels, [])
        for x in range(size0):
            AppendPIL(pixels, x, y, data)
    return pixels


def SortImage(pixels, intervals, args, sorting_function):
    r"""
    Sorts the image.
    -----
    :param pixels: List of pixel values.
    :param intervals: List of pixel values after being run through selected interval function.
    :param args: Arguments.
    :param sorting_function: Sorting function used in sorting of pixels.
    :returns: List of sorted pixels.
    """
    sorted_pixels = []
    sort_interval = lambda lst, func: [] if lst == [] else sorted(lst, key=func)
    for y in ProgressBars(len(pixels), "Sorting..."):
        row = []
        x_min = 0
        for x_max in intervals[y]:
            interval = []
            for x in range(x_min, x_max):
                Append3D(interval, x, y, pixels)
            if rand.randint(0, 100) >= args["randomness"]:
                row += sort_interval(interval, sorting_function)
            else:
                row += interval
            x_min = x_max
        Append3D(row, 0, y, pixels)
        Append(sorted_pixels, row)
    return sorted_pixels
