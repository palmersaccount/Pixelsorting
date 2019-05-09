# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as rand
from typing import Any, Callable, List

from MiscLambdas import Append, AppendList, ProgressBars


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
