# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import random as rand
import socket
import sys
from colorsys import rgb_to_hsv
from datetime import datetime
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any, Callable, List, Tuple

import numpy as np
from PIL import Image, ImageFilter
from requests import get, post
from tqdm import tqdm

from MiscFuncs import HasInternet, PixelAppend, ElementaryCA, UploadImg, CropTo
from MiscLambdas import (
    black_pixel,
    white_pixel,
    ImgOpen,
    Append,
    AppendPIL,
    AppendList,
    AppendPartial,
    ImgPixels,
    RandomWidth,
    ProgressBars,
    AppendBW,
    IDGen,
)
from intervals import (
    random,
    threshold,
    edge,
    waves,
    snap_sort,
    file_mask,
    file_edges,
    shuffle_total,
    shuffled_axis,
    none,
)

# SORTING PIXELS #
lightness: Callable[[Any], float] = (lambda p: rgb_to_hsv(p[0], p[1], p[2])[2] / 255.0)
intensity: Callable[[Any], float] = lambda p: p[0] + p[1] + p[2]
hue: Callable[[Any], float] = lambda p: rgb_to_hsv(p[0], p[1], p[2])[0] / 255.0
saturation: Callable[[Any], float] = (lambda p: rgb_to_hsv(p[0], p[1], p[2])[1] / 255.0)
minimum: Callable[[Any], float] = lambda p: min(p[0], p[1], p[2])

# SORTER #
def SortImage(
    pixels: List, intervals: List, args: Any, sorting_function: Callable[[Any], float]
) -> List:
    """
    Sorts the image.
    -----
    :param pixels: List of pixel values.
    :param intervals: List of pixel values after being run through selected interval function.
    :param args: Arguments.
    :param sorting_function: Sorting function used in sorting of pixels.
    :returns: List of sorted pixels.
    """
    sorted_pixels: List = []
    sort_interval: Callable[[List[Any], Callable[[Any], float]], List[Any]] = (
        lambda lst, func: [] if lst == [] else sorted(lst, key=func)
    )
    for y in ProgressBars(len(pixels), "Sorting..."):
        row: List = []
        x_min = 0
        for x_max in intervals[y]:
            interval: List = []
            for x in range(x_min, x_max):
                AppendList(interval, x, y, pixels)
            if rand.randint(0, 100) >= args.randomness:
                row += sort_interval(interval, sorting_function)
            else:
                row += interval
            x_min = x_max
        AppendList(row, 0, y, pixels)
        Append(sorted_pixels, row)
    return sorted_pixels
