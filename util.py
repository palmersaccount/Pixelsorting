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

from PIL import Image
from requests import get, post

from pixelsort import trange
from sorting import lightness

BlackPixel = (0, 0, 0, 255)
WhitePixel = (255, 255, 255, 255)


def clear():
    r"""
    Clears the screen when called.
    :return: OS system call to clear the screen based on os type.
    """
    return system("cls" if name == "nt" else "clear")


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


def CropTo(image_to_crop, args):
    r"""
    Crops image to the size of a reference image. This function assumes
    that the relevant image is located in the center and you want to crop away
    equal sizes on both the left and right as well on both the top and bottom.
    :param image_to_crop
    :param reference_image
    :return: image cropped to the size of the reference image
    """
    reference_image = ImgOpen(args["url"], args["internet"])
    reference_size = reference_image.size
    current_size = image_to_crop.size
    dx = current_size[0] - reference_size[0]
    dy = current_size[1] - reference_size[1]
    left = dx / 2
    upper = dy / 2
    right = dx / 2 + reference_size[0]
    lower = dy / 2 + reference_size[1]
    return image_to_crop.crop(box=(int(left), int(upper), int(right), int(lower)))


def ImgOpen(url, internet=HasInternet()):
    r"""
    Opens the image from a direct url if the internet is connected.
    ------
    :param url: The URL of a direct image.
    :param internet: a bool if the internet is connected.
    :returns: Callable 'Image' object from Pillow.

    Example
    -----
    >>> img = ImgOpen(url, internet)
    >>> img
    >>> <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=2560x1974 at 0x29C74D7A518>
    """
    try:
        img = Image.open((get(url, stream=True).raw) if internet else url).convert(
            "RGBA"
        )
        return img
    except OSError:
        print(
            f"{'---'*15}\nURL '{url}' not usable!\nPlease find the direct image url to use this script!\n{'---'*15}"
        )
        exit()


def UploadImg(img):
    r"""
    Upload an image to put.re
    -----
    :param img: A string of a local file.
    :returns: String of link of the uploaded file.

    Example
    -----
    >>> link = UploadImg("https://i.redd.it/ufj4p5zwf9v21.jpg")
    >>> link
    >>> "https://s.put.re/Uc2A2Z7t.jpg"
    (those links are actually correct.)
    """
    try:
        r = post("https://api.put.re/upload", files={"file": (img, open(img, "rb"))})
        output = loads(r.text)
        link: str = output["data"]["link"]
        return link
    except FileNotFoundError:
        print(f"{'---'*15}\n'{img}' not usable!\n{'---'*15}")
        exit()


# LAMBDA FUNCTIONS #
RandomWidthlambda = lambda c: int(c * (1 - rand.random()))
IDGen = lambda length: "".join(
    rand.choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(length)
)
ProgressBars = lambda r, desc: trange(r, desc=("{:30}".format(desc)))

# lambda rewrites
def RemoveOld(fileName):
    """
    Removes a file
    ---
    Args:
        fileName (str): Name of the file to be removed
    """
    if path.exists(fileName):
        remove(fileName)


def Append(listName, obj):
    """Append an object in place.
    ---
    improves effeciency a lot more than one would think.

    :param listName: name of the list
    :param obj: object being appended
    """
    listName.append(obj)


def AppendPIL(listName, x, y, data):
    """Append in place a PIL pixel value, obtained from a PIL data object
    ---
    :param listName: name of the list
    :param x: x position
    :param y: y position
    :param data: data object, obtained from Image.load()
    """
    listName[y].append(data[x, y])


def Append3D(listName, x, y, data):
    """Appends an object in y position in a 3 dimensional list
    ---
    commonly used for image lists
    
    :param listName: name of the list
    :param x: x position
    :param y: y position
    :param data: obtained from Image.load()
    """
    listName.append(data[y][x])


def AppendInPlace(listName, y, obj):
    """Appends an object in list 'y'
    ---
    :param listName: name of list
    :param y: position y
    :param obj: object being appended
    """
    listName[y].append(obj)


def ImgPixels(img, x, y, data):
    """Puts pixels backa into an image from a 3D list
    ---
    :param img: image (usually blank)
    :param x: position x
    :param y: position y
    :param data: data object, obtained from Image.load()
    """
    img.putpixel((x, y), data[y][x])


def AppendBW(listName, x, y, data, threshold):
    """Appends a pixel in place based on a threshold value as well as the values of a black and white pixel
    ---
    
    :param listName: name of the list
    :param x: position x
    :param y: position y
    :param data: obtained from Image.load()
    :param threshold: threshold value
    """
    BlackPixel = (0, 0, 0, 255)
    WhitePixel = (255, 255, 255, 255)

    if lightness(data[y][x]) < threshold:
        AppendInPlace(listName, y, WhitePixel)
    else:
        AppendInPlace(listName, y, BlackPixel)
