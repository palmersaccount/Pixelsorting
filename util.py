"""
This is where all the utility related functions go, like checking for internet and clearing the terminal.

ALl lambda functions are also contained here, with the exceoption of the lambdas used for sorting pixels.
"""

import argparse
import random as rand
import socket
from colorsys import rgb_to_hsv
from datetime import datetime
from json import dumps, loads
from os import name, path, remove, system
from string import ascii_lowercase, ascii_uppercase, digits
from subprocess import run
from urllib.parse import urlparse

from pixelsort import trange
from sorting import lightness

BlackPixel = (0, 0, 0, 255)
WhitePixel = (255, 255, 255, 255)


def HasInternet(host: str = "1.1.1.1", port: int = 53, timeout: int = 3) -> bool:
    r"""
    Checks for internet.
    ------
    :param host: 1.1.1.1 (Cloudfare public DNS)
    :param port: 53
    :param timeout: 3

    Service: domain (DNS/TCP)

    Example
    ------
    >>> internet = HasInternet("1.1.1.1", 53, 3)
    >>> internet
    >>> True
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


# LAMBDA FUNCTIONS #
RemoveOld = lambda f: remove(f) if path.exists(f) else None
Append = lambda l, obj: l.append(obj)
AppendPIL = lambda l, x, y, d: l[y].append(d[x, y])
Append3D = lambda l, x, y, d: l.append(d[y][x])
AppendInPlace = lambda l, y, x: l[y].append(x)
RandomWidthlambda = lambda c: int(c * (1 - rand.random()))
ImgPixels = lambda i, x, y, d: i.putpixel((x, y), d[y][x])
IDGen = lambda length: "".join(
    rand.choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(length)
)
ProgressBars = lambda r, desc: trange(r, desc=("{:30}".format(desc)))
AppendBW = (
    lambda lst, x, y, data, thresh: AppendInPlace(lst, y, WhitePixel)
    if (lightness(data[y][x]) < thresh)
    else AppendInPlace(lst, y, BlackPixel)
)
