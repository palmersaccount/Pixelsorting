# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random as rand
import socket
from typing import Any, List, Tuple

from PIL import Image
from requests import post

from MiscLambdas import Append, AppendPartial, AppendPIL, ImgOpen, ProgressBars


def HasInternet(host: str, port: int, timeout: int) -> bool:
    """
    Checks for internet.
    ------
    :param host: 8.8.8.8 (google-public-dns-a.google.com)
    :param port: 53
    :param timeout: 3

    Service: domain (DNS/TCP)

    Examples
    ------
    >>> internet = HasInternet("8.8.8.8", 53, 3)
    >>> print(internet)
    True
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def PixelAppend(size1: int, size0: int, data: Any, msg: str) -> List:
    """
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
    pixels: List = []
    for y in ProgressBars(size1, msg):
        Append(pixels, [])
        for x in range(size0):
            AppendPIL(pixels, x, y, data)
    return pixels


def ElementaryCA(pixels: Any) -> Any:
    """
    Generate images of elementary cellular automata.
    Selected rules from https://en.wikipedia.org/wiki/Elementary_cellular_automaton
    ------
    :param pixels: 2D list of RGB values.
    :returns: PIL Image object.
    """
    width: int = rand.randrange(100, 150)
    height: int = rand.randrange(100, 150)
    ruleprompt: Any = input(
        f"Rule selection (max of 255)(leave blank for random)\n"
        f"(Recommended to leave blank, most of the rules aren't good): "
    )
    try:
        if int(ruleprompt) in range(255):
            rulenumber: int = int(ruleprompt)
    except ValueError:
        rules: List = [26, 19, 23, 25, 35, 106, 11, 110, 45, 41, 105, 54, 3, 15, 9, 154]
        rulenumber = rules[rand.randrange(0, len(rules))]

    scalefactor: int = rand.randrange(1, 5)

    # Define colors of the output image
    true_pixel: Tuple[int, int, int] = (255, 255, 255)
    false_pixel: Tuple[int, int, int] = (0, 0, 0)

    # Generates a dictionary that tells you what your state should be based on the rule number
    # and the states of the adjacent cells in the previous generation
    def generate_rule(rulenumber: int) -> dict:
        rule: dict = {}
        for left in [False, True]:
            for middle in [False, True]:
                for right in [False, True]:
                    rule[(left, middle, right)] = rulenumber % 2 == 1
                    rulenumber //= 2
        return rule

    # Generates a 2d representation of the state of the automaton at each generation
    def generate_ca(rule: dict) -> List:
        ca: List = []
        # Initialize the first row of ca randomly
        Append(ca, [])
        for x in range(width):
            AppendPartial(ca, 0, bool(rand.getrandbits(1)))

        # Generate the succeeding generation
        # Cells at the eges are initialized randomly
        for y in range(1, height):
            Append(ca, [])
            AppendPartial(ca, y, bool(rand.getrandbits(1)))
            for x in range(1, width - 1):
                AppendPartial(
                    ca, y, (rule[(ca[y - 1][x - 1], ca[y - 1][x], ca[y - 1][x + 1])])
                )
            AppendPartial(ca, y, bool(rand.getrandbits(1)))
        return ca

    rule = generate_rule(rulenumber)
    ca = generate_ca(rule)

    newImg = Image.new("RGB", [width, height])

    print(f"Creating file image..\nRule: {rulenumber}")
    for y in ProgressBars(height, "Placing pixels..."):
        for x in range(width):
            newImg.putpixel(
                (x, y),
                true_pixel
                if ca[int(y / scalefactor)][int(x / scalefactor)]
                else false_pixel,
            )

    print("File image created!")
    newImg.save("images/ElementaryCA.png")
    return newImg


def UploadImg(img: str) -> str:
    """
    Upload an image to put.re
    -----
    :param img: A string of a local file.
    :returns: String of link of the uploaded file.
    
    Example
    -----
    >>> link = UploadImg("https://i.redd.it/ufj4p5zwf9v21.jpg")
    >>> print(link)
    >>> "https://s.put.re/Uc2A2Z7t.jpg"
    (those links are actually correct.)
    """
    r = post("https://api.put.re/upload", files={"file": (img, open(img, "rb"))})
    output = json.loads(r.text)
    link: str = output["data"]["link"]
    return link


def CropTo(image_to_crop: Any, args: Any) -> Any:
    """
    Crops image to the size of a reference image. This function assumes
    that the relevant image is located in the center and you want to crop away
    equal sizes on both the left and right as well on both the top and bottom.
    :param image_to_crop
    :param reference_image
    :return: image cropped to the size of the reference image
    """
    reference_image = ImgOpen(args.url, args.internet)
    reference_size: Tuple[int, int] = reference_image.size
    current_size: Tuple[int, int] = image_to_crop.size
    dx = current_size[0] - reference_size[0]
    dy = current_size[1] - reference_size[1]
    left = dx / 2
    upper = dy / 2
    right = dx / 2 + reference_size[0]
    lower = dy / 2 + reference_size[1]
    return image_to_crop.crop(box=(int(left), int(upper), int(right), int(lower)))
