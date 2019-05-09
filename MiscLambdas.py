# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as rand
from colorsys import rgb_to_hsv
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any, Callable, List, Tuple

from PIL import Image
from requests import get
from tqdm import tqdm

# SORTING PIXELS #
lightness: Callable[[Any], float] = (lambda p: rgb_to_hsv(p[0], p[1], p[2])[2] / 255.0)
intensity: Callable[[Any], float] = lambda p: p[0] + p[1] + p[2]
hue: Callable[[Any], float] = lambda p: rgb_to_hsv(p[0], p[1], p[2])[0] / 255.0
saturation: Callable[[Any], float] = (lambda p: rgb_to_hsv(p[0], p[1], p[2])[1] / 255.0)
minimum: Callable[[Any], float] = lambda p: min(p[0], p[1], p[2])

black_pixel: Tuple[int, int, int, int] = (0, 0, 0, 255)
white_pixel: Tuple[int, int, int, int] = (255, 255, 255, 255)

# LAMBDA FUNCTIONS #
ImgOpen: Callable[[str, bool], Any] = lambda u, i: (
    Image.open((get(u, stream=True).raw) if i else u)
).convert("RGBA")
Append: Callable[[Any, Any], Any] = lambda l, obj: l.append(obj)
AppendPIL: Callable[[Any, int, int, Any], Any] = lambda l, x, y, d: l[y].append(d[x, y])
AppendList: Callable[[List, int, int, Any], Any] = lambda l, x, y, d: l.append(d[y][x])
AppendPartial: Callable[[List, int, Any], List] = lambda l, y, x: l[y].append(x)
ImgPixels: Callable[[Any, int, int, Any], Any] = lambda i, x, y, d: i.putpixel(
    (x, y), d[y][x]
)
RandomWidth: Callable[[int], int] = lambda c: int(c * (1 - rand.random()))
ProgressBars: Callable[[Any, str], Any] = lambda r, d: tqdm(
    range(r), desc=("{:30}".format(d))
)
AppendBW: Callable[[List, int, int, Any, float], List] = (
    lambda l, x, y, d, t: AppendPartial(l, y, white_pixel)
    if (lightness(d[y][x]) < t)
    else AppendPartial(l, y, black_pixel)
)

# UTIL #
IDGen: Callable[[int], str] = lambda n: "".join(
    rand.choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(n)
)
