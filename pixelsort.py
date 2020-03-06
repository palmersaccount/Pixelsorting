# !/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def HasInternet(host="1.1.1.1", port=53, timeout=3):
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


try:
    from numpy import array, mgrid
    from numpy.random import choice, shuffle
    from PIL import Image, ImageFilter
    from requests import get, post, request
    from tqdm import tqdm, trange
except ImportError:
    if HasInternet():
        # Upgrade/Install all packages
        run(["pip", "install", "pillow", "numpy", "tqdm", "requests", "--upgrade"])
        from numpy import array, mgrid
        from numpy.random import choice, shuffle
        from PIL import Image, ImageFilter
        from requests import get, post, request
        from tqdm import tqdm, trange
    else:
        print(
            "Dependecies not installed! Unable to install any automatically, script is unable to function without them."
        )
        exit()


BlackPixel = (0, 0, 0, 255)
WhitePixel = (255, 255, 255, 255)


# LAMBDA FUNCTIONS #
RemoveOld = lambda f: remove(f) if path.exists(f) else None
Append = lambda l, obj: l.append(obj)
AppendPIL = lambda l, x, y, d: l[y].append(d[x, y])
Append3D = lambda l, x, y, d: l.append(d[y][x])
AppendInPlace = lambda l, y, x: l[y].append(x)
RandomWidth = lambda c: (c * (1 - rand.random()))
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


# SORTING PIXELS #
lightness = lambda p: rgb_to_hsv(p[0], p[1], p[2])[2] / 255.0
intensity = lambda p: p[0] + p[1] + p[2]
hue = lambda p: rgb_to_hsv(p[0], p[1], p[2])[0] / 255.0
saturation = lambda p: rgb_to_hsv(p[0], p[1], p[2])[1] / 255.0
minimum = lambda p: min(p[0], p[1], p[2])


# MISC FUNCTIONS #
def clear():
    r"""
    Clears the screen when called.
    :return: OS system call to clear the screen based on os type.
    """
    return system("cls" if name == "nt" else "clear")


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


def ElementaryCA(pixels, args, width, height):
    r"""
    Generate images of elementary cellular automata.
    Selected rules from https://en.wikipedia.org/wiki/Elementary_cellular_automaton
    ------
    :param pixels: 2D list of RGB values.
    :param args: namespace of arguments.
    :param width: used for image size.
    :param height: used for image size.
    :returns: PIL Image object.
    """
    width /= 4 if width <= 2500 else 8
    height /= 4 if height <= 2500 else 8
    if args["filelink"] in ["False", ""]:
        rules = [26, 19, 23, 25, 35, 106, 11, 110, 45, 41, 105, 54, 3, 15, 9, 154, 142]

        if args["presetname"] not in ["Snap", "Random"]:
            ruleprompt = input(
                f"Rule selection (max of 255)(leave blank for random)\n"
                f"(Recommended to leave blank, most of the rules aren't good): "
            )
            try:
                if int(ruleprompt) in range(255):
                    rulenumber = int(ruleprompt)
                else:
                    print("Number not in range, using random rule.")
                    rulenumber = rules[rand.randrange(0, len(rules))]
            except ValueError:
                rulenumber = rules[rand.randrange(0, len(rules))]
        else:
            rulenumber = rules[rand.randrange(0, len(rules))]

        scalefactor = 1

        # Define colors of the output image
        true_pixel = (255, 255, 255)
        false_pixel = (0, 0, 0)

        # Generates a dictionary that tells you what your state should be based on the rule number
        # and the states of the adjacent cells in the previous generation
        def generate_rule(rulenumber) -> dict:
            rule = {}
            for left in [False, True]:
                for middle in [False, True]:
                    for right in [False, True]:
                        rule[(left, middle, right)] = rulenumber % 2 == 1
                        rulenumber //= 2
            return rule

        # Generates a 2d representation of the state of the automaton at each generation
        def generate_ca(rule):
            ca = []
            # Initialize the first row of ca randomly
            Append(ca, [])
            for x in range(int(width)):
                AppendInPlace(ca, 0, bool(rand.getrandbits(1)))

            # Generate the succeeding generation
            # Cells at the eges are initialized randomly
            for y in range(1, int(height)):
                Append(ca, [])
                AppendInPlace(ca, y, bool(rand.getrandbits(1)))
                for x in range(1, int(width) - 1):
                    AppendInPlace(
                        ca,
                        y,
                        (rule[(ca[y - 1][x - 1], ca[y - 1][x], ca[y - 1][x + 1])]),
                    )
                AppendInPlace(ca, y, bool(rand.getrandbits(1)))
            return ca

        rule = generate_rule(rulenumber)
        ca = generate_ca(rule)

        newImg = Image.new("RGB", [int(width), int(height)])

        print(f"Creating file image..\nRule: {rulenumber}")
        for y in ProgressBars(int(height), "Placing pixels..."):
            for x in range(int(width)):
                newImg.putpixel(
                    (x, y),
                    true_pixel
                    if ca[int(y / scalefactor)][int(x / scalefactor)]
                    else false_pixel,
                )

        print("File image created!")
        newImg.save("images/ElementaryCA.png")
        return newImg
    else:
        print("Using file image from DB...")
        img = ImgOpen(args["filelink"], args["internet"])
        img.save("images/ElementaryCA.png")
        return img


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
        link = output["data"]["link"]
        return link, True
    except FileNotFoundError:
        print(f"{'---'*15}\n'{img}' not usable!\n{'---'*15}")
        return "", False
    except KeyError:
        print(f"{'---'*15}\n{output['message']}\n{'---'*15}")
        print(f"\n\nput.re's API is currently down. Sorry about that.")
        return "", False


def ImgOpen(url, internet):
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


# READING FUNCTIONS #
def ReadImageInput(url_input, misc_variables, internet=HasInternet()):
    r"""
    Reading the image input.
    -----
    :param url_input: The inputted URL, number of default image, or local file path.
    :param internet: true/false for having internet.
    :returns: (in order) url[str], url_given[bool], url_random[bool], random_url[str]

    Explination on returns:
    - url -> the url or local image string.
    - url_given -> was the url given? or randomized?
    - url_random -> was the url randomized or chosen from preset images?
    - random_url -> if the url was randomly chose, the string of what number was chosen
    """
    print("Opening image...")
    url_options = {
        "0": "https://s.put.re/SRcqAfhP.jpg",
        "1": "https://s.put.re/Ds9KV8jX.jpg",
        "2": "https://s.put.re/QsUQbC1R.jpg",
        "3": "https://s.put.re/5zgcV3TT.jpg",
        "4": "https://s.put.re/567w8wpK.jpg",
        "5": "https://s.put.re/gcYkpmbd.jpg",
        "6": "https://s.put.re/K49iqXVJ.png",
    }
    random_url = str(rand.randint(0, len(url_options)))
    img_parse = urlparse(url_input)

    try:
        assert url_input not in ["0", "1", "2", "3", "4", "5", "6"]
        if internet and url_input not in ["", " "]:
            if img_parse.scheme not in ["http", "https"]:
                print("Local image detected! Uploading to put.re...")
                url_input, misc_variables["image_upload_failed"] = UploadImg(url_input)
                return url_input, True, False, random_url
            ImgOpen(url_input, internet)
            return url_input, True, False, None
        else:
            if url_input in ["", " "]:
                print("Using included default image")
                url = (
                    UploadImg("images/default.jpg")
                    if internet
                    else "images/default.jpg"
                )
            else:
                url = url_input
            return url, True, False, False
    except (IOError, AssertionError):
        try:
            return (
                (
                    url_options[
                        (
                            url_input
                            if url_input in ["0", "1", "2", "3", "4", "5", "6"]
                            else random_url
                        )
                    ]
                    if url_input in ["", " ", "0", "1", "2", "3", "4", "5", "6"]
                    else url_input
                ),
                (
                    False
                    if url_input in ["", " ", "0", "1", "2", "3", "4", "5", "6"]
                    else True
                ),
                (True if url_input in ["", " "] else False),
                (random_url if url_input in ["", " "] else None),
            )
        except KeyError:
            return url_options[random_url], False, True, random_url


def ReadIntervalFunction(int_func_input):
    r"""
    Reading the interval function.
    -----
    :param int_func_input: A (lowercase) string.
    :returns: Interval function.
    :raises KeyError: String not in selection.

    Example
    -----
    >>> interval = ReadIntervalFunction("random")
    >>> interval
    >>> function<random>
    """
    try:
        return {
            "random": random,
            "threshold": threshold,
            "edges": edge,
            "waves": waves,
            "snap": snap_sort,
            "file": file_mask,
            "file-edges": file_edges,
            "shuffle-total": shuffle_total,
            "shuffle-axis": shuffled_axis,
            "none": none,
        }[int_func_input]
    except KeyError:
        return random


def ReadSortingFunction(sort_func_input):
    r"""
    Reading the sorting function.
    -----
    :param sort_func_input: A (lowercase) string.
    :returns: Sorting function.
    :raises KeyError: String not in selection.

    Example
    -----
    >>> sortFunc = ReadSortingFunction("hue")
    >>> sortFunc
    >>> lambda<hue>
    """
    try:
        return {
            "lightness": lightness,
            "hue": hue,
            "intensity": intensity,
            "minimum": minimum,
            "saturation": saturation,
        }[sort_func_input]
    except KeyError:
        return lightness


def ReadPreset(preset_input, width, presets):
    r"""
    Returning values for 'presets'.
    -----
    :param preset_input: A (lowercase) string.
    :param width: the input img width, used for size reference
    :returns: (in order) arg_parse_input, int_func_input, sort_func_input, preset_true, int_rand, sort_rand, int_chosen, sort_chosen, shuffled, snapped, file_sorted, db_preset, db_file_img
    :raises KeyError: String not in selection.

    Explination of returns
    -----
    - arg_parse_input -> what the arg parse input is
    - int_func_input -> what the chosen interval function is
    - sort_func_input -> what the sorting function is
    - preset_true -> is the preset true
    - int_rand -> was the interval function chosen at random?
    - sort_rand -> was the sorting function chosen at random?
    - int_chosen -> was the interval function chosen chosen?
    - sort_chosen -> was the sorting function chosen?
    - shuffled -> is the interval function shuffled?
    - snapped -> is the interval function snapped?
    - file_sorted -> is the interval function file?
    - db_preset -> is the preset gathered from the database?
    - db_file_img -> if the preset is from the database, the file image link
    """
    try:
        # order-- arg_parse_input, int_func_input, sort_func_input, preset_true, int_rand, sort_rand, int_chosen, sort_chosen, shuffled, snapped, file_sorted, db_preset, db_file_img
        if HasInternet():
            r = get(
                "https://pixelsorting-a289.restdb.io/rest/outputs",
                headers={
                    "Content-Type": "application/json",
                    "x-apikey": "acc71784a255a80c2fd25e081890a1767edaf",
                },
            )
            for data in r.json():
                try:
                    if preset_input in data["preset_id"]:
                        return (
                            data["args"],
                            data["int_func"],
                            data["sort_func"],
                            True,
                            False,
                            False,
                            True,
                            True,
                            (
                                True
                                if data["int_func"] in ["shuffle-total", "shuffle-axis"]
                                else False
                            ),
                            (True if data["int_func"] in ["snap"] else False),
                            (
                                True
                                if data["int_func"] in ["file", "file-edges"]
                                else False
                            ),
                            True,
                            data["file_link"],
                        )
                except KeyError:
                    continue
        print(presets[preset_input][1])
        return presets[preset_input][1]
    except KeyError:
        print("[WARNING] Invalid preset name, no preset will be applied")
        return (
            "",
            "",
            "",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "",
        )


# SORTER #
def SortImage(pixels, intervals, args, sorting_function):
    r"""
    Sorts the image.
    -----
    :param pixels of pixel values.
    :param intervals of pixel values after being run through selected interval function.
    :param args: Arguments.
    :param sorting_function: Sorting function used in sorting of pixels.
    :returns of sorted pixels.
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


# INTERVALS #
def edge(pixels, args):
    edge_data = (
        ImgOpen(args["url"], args["internet"])
        .rotate(args["angle"], expand=True)
        .filter(ImageFilter.FIND_EDGES)
        .convert("RGBA")
        .load()
    )

    filter_pixels = PixelAppend(
        len(pixels), len(pixels[0]), edge_data, "Finding threshold..."
    )
    edge_pixels = []
    intervals = []

    for y in ProgressBars(len(pixels), "Thresholding..."):
        Append(edge_pixels, [])
        for x in range(len(pixels[0])):
            AppendBW(edge_pixels, x, y, filter_pixels, args["bottom_threshold"])

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if edge_pixels[y][x] == BlackPixel and edge_pixels[y][x - 1] == BlackPixel:
                edge_pixels[y][x] = WhitePixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == BlackPixel:
                AppendInPlace(intervals, y, x)
        AppendInPlace(intervals, y, len(pixels[0]))
    return intervals


def threshold(pixels, args):
    intervals = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if (
                lightness(pixels[y][x]) < args["bottom_threshold"]
                or lightness(pixels[y][x]) > args["upper_threshold"]
            ):
                AppendInPlace(intervals, y, x)
        AppendInPlace(intervals, y, len(pixels[0]))
    return intervals


def random(pixels, args):
    intervals = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        x = 0
        while True:
            width = RandomWidth(args["clength"])
            x += width
            if x > len(pixels[0]):
                AppendInPlace(intervals, y, len(pixels[0]))
                break
            else:
                AppendInPlace(intervals, y, x)
    return intervals


def waves(pixels, args):
    intervals = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        x = 0
        while True:
            width = args["clength"] + rand.randint(0, 10)
            x += width
            if x > len(pixels[0]):
                AppendInPlace(intervals, y, len(pixels[0]))
                break
            else:
                AppendInPlace(intervals, y, x)
    return intervals


def file_mask(pixels, args):
    img = ElementaryCA(pixels, args, int(len(pixels)), int(len(pixels[0]))).resize(
        (len(pixels[0]), len(pixels)), Image.ANTIALIAS
    )
    data = img.load()

    file_pixels = PixelAppend(len(pixels), len(pixels[0]), data, "Defining edges...")
    intervals = []

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up edges..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if file_pixels[y][x] == BlackPixel and file_pixels[y][x - 1] == BlackPixel:
                file_pixels[y][x] = WhitePixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if file_pixels[y][x] == BlackPixel:
                AppendInPlace(intervals, y, x)
        AppendInPlace(intervals, y, len(pixels[0]))

    return intervals


def file_edges(pixels, args):
    edge_data = (
        ElementaryCA(pixels, args, int(len(pixels)), int(len(pixels[0])))
        .rotate(args["angle"], expand=True)
        .resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
        .filter(ImageFilter.FIND_EDGES)
        .convert("RGBA")
        .load()
    )

    filter_pixels = PixelAppend(
        len(pixels), len(pixels[0]), edge_data, "Defining edges..."
    )
    edge_pixels = []
    intervals = []

    for y in ProgressBars(len(pixels), "Thresholding..."):
        Append(edge_pixels, [])
        for x in range(len(pixels[0])):
            AppendBW(edge_pixels, x, y, filter_pixels, args["bottom_threshold"])

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up edges..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if edge_pixels[y][x] == BlackPixel and edge_pixels[y][x - 1] == BlackPixel:
                edge_pixels[y][x] = WhitePixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == BlackPixel:
                AppendInPlace(intervals, y, x)
        AppendInPlace(intervals, y, len(pixels[0]))
    return intervals


def snap_sort(pixels, args):
    input_img = ImgOpen("images/thanos_img.png", False)
    pixels_snap = array(input_img)

    print("The hardest choices require the strongest wills...")
    nx, ny = input_img.size
    xy = mgrid[:nx, :ny].reshape(2, -1).T
    rounded = int(round(int(xy.shape[0] / 2), 0))

    numbers_that_dont_feel_so_good = xy.take(
        choice(xy.shape[0], rounded, replace=False), axis=0
    )
    print(f'Number of those worthy of the sacrifice: {("{:,}".format(rounded))}')

    for i in ProgressBars(len(numbers_that_dont_feel_so_good), "Snapping..."):
        pixels_snap[numbers_that_dont_feel_so_good[i][1]][
            numbers_that_dont_feel_so_good[i][0]
        ] = [0, 0, 0, 0]

    print("Sorted perfectly in half.")
    returned_souls = Image.fromarray(pixels_snap, "RGBA")
    returned_souls.save("images/snapped_pixels.png")

    snapped_img = ImgOpen("images/snapped_pixels.png", False)
    data = snapped_img.load()
    size0, size1 = snapped_img.size
    pixels_return = PixelAppend(size1, size0, data, "I hope they remember you...")

    RemoveOld("images/snapped_pixels.png")
    RemoveOld("images/thanos_img.png")
    print(f"{('/' * 45)}\nPerfectly balanced, as all things should be.\n{('/' * 45)}")

    return pixels_return


def shuffle_total(pixels, args):
    print("Creating array from image...")
    input_img = ImgOpen(args["url"], args["internet"]).convert("RGBA")
    height = input_img.size[1]
    shuffled = array(input_img)

    for i in ProgressBars(int(height), "Shuffling image..."):
        shuffle(shuffled[i])
    print("Saving shuffled image...")
    shuffled_img = Image.fromarray(shuffled, "RGBA")
    data = shuffled_img.load()

    size0, size1 = input_img.size
    pixels = PixelAppend(size1, size0, data, "Recreating image...")

    RemoveOld("images/shuffled.png")
    return pixels


def shuffled_axis(pixels, args):
    print("Creating array from image...")
    input_img = ImgOpen(args["url"], args["internet"]).convert("RGBA")
    height = input_img.size[1]
    shuffled = array(input_img)

    for _ in ProgressBars(height, "Shuffling image..."):
        shuffle(shuffled)
    print("Saving shuffled image...")
    shuffled_img = Image.fromarray(shuffled, "RGBA")
    data = shuffled_img.load()

    size0, size1 = input_img.size
    pixels = PixelAppend(size1, size0, data, "Recreating image...")

    RemoveOld("images/shuffled.png")
    return pixels


def none(pixels, args):
    intervals = []
    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [len(pixels[y])])
    return intervals


# MAIN #
def main():
    """
    Pixelsorting an image.
    """

    # arg parsing arguments
    parse = argparse.ArgumentParser(description="pixel mangle an image")
    parse_util = argparse.ArgumentParser(description="misc. args used in program")
    """
    (Taken args)
    //user read//
    :-t,--bottom_threshold -> bottom/lower threshold
    :-u,--upper_threshold -> top/upper threshold
    :-c,--clength -> character length
    :-a,--angle -> angle for rotation
    :-r,--randomness -> randomness

    //not accessible to user//
    :-l,--url -> url
    :-i,--int_function -> interval function
    :-s,--sorting_function -> sorting function
    :-p --preset -> is preset used
    :-d --dbpreset -> is dbpreset used
    :-y --internet -> is internet there
    :-k --filelink -> for DBpreset
    :-b --presetname -> name of preset used
    """
    parse.add_argument(
        "-t",
        "--bottom_threshold",
        type=float,
        help="Pixels darker than this are not sorted, between 0 and 1",
        default=0.25,
    )
    parse.add_argument(
        "-u",
        "--upper_threshold",
        type=float,
        help="Pixels darker than this are not sorted, between 0 and 1",
        default=0.8,
    )
    parse.add_argument(
        "-c",
        "--clength",
        type=int,
        help="Characteristic length of random intervals",
        default=50,
    )
    parse.add_argument(
        "-a",
        "--angle",
        type=float,
        help="Rotate the image by an angle (in degrees) before sorting",
        default=0,
    )
    parse.add_argument(
        "-r",
        "--randomness",
        type=float,
        help="What percentage of intervals are NOT sorted",
        default=10,
    )

    parse_util.add_argument(
        "-l",
        "--url",
        help="URL of a given image. Used as the input image.",
        default="https://s.put.re/QsUQbC1R.jpg",
    )
    parse_util.add_argument(
        "-i",
        "--int_function",
        help="random, threshold, edges, waves, snap, shuffle-total, shuffle-axis, file, file-edges, none",
        default="random",
    )
    parse_util.add_argument(
        "-s",
        "--sorting_function",
        help="lightness, intensity, hue, saturation, minimum",
        default="lightness",
    )
    parse_util.add_argument(
        "-p",
        "--preset",
        type=bool,
        help="Is a preset used or not? Boolean.",
        default=False,
    )
    parse_util.add_argument(
        "-d",
        "--dbpreset",
        help="Boolean for if preset is used or not.",
        type=bool,
        default=False,
    )
    parse_util.add_argument(
        "-y",
        "--internet",
        help="Boolean for if internet is preset or not.",
        type=bool,
        default=True,
    )
    parse_util.add_argument(
        "-b", "--presetname", help="Name of the preset used.", default="None"
    )
    parse_util.add_argument(
        "-k", "--filelink", help="File image used, only in DB preset mode.", default=""
    )

    clear()
    # remove old image files that didn't get deleted before
    ##RemoveOld("images/image.png")
    RemoveOld("images/thanos_img.png")
    RemoveOld("images/snapped_pixels.png")
    RemoveOld("images/ElementaryCA.png")

    # variables
    misc_variables = {
        "internet": HasInternet(),
        "preset_true": False,
        "snapped": False,
        "shuffled": False,
        "int_rand": False,
        "sort_rand": False,
        "int_chosen": False,
        "sort_chosen": False,
        "file_sorted": False,
        "image_upload_failed": False,
        "resolution_msg": "",
        "image_msg": "",
        "int_msg": "",
        "sort_msg": "",
        "site_msg": "",
        "link": "",
        "date_time": datetime.now().strftime("%m/%d/%Y %H:%M"),
        "preset_id": datetime.now().strftime("%m%d%Y%H%M"),
        "sort_func_options": ["lightness", "hue", "intensity", "minimum", "saturation"],
        "int_func_options": [
            "random",
            "threshold",
            "edges",
            "waves",
            "snap",
            "file",
            "file-edges",
            "none",
            "shuffle-total",
            "shuffle-axis",
        ],
    }
    presets = {
        "Main": [
            "Main args (r: 35-65, c: random gen, a: 0-360, random, intensity)",
            (
                (
                    f"-r {rand.randrange(35, 65)} "
                    f"-c {(rand.randrange(150, 350, 25))} "
                    f"-a {rand.randrange(0, 360)} "
                ),
                "random",
                "intensity",
                True,
                False,
                False,
                True,
                True,
                False,
                False,
                False,
                False,
                "",
            ),
        ],
        "File": [
            "Main args, but only for file edges",
            (
                (
                    f"-r {rand.randrange(15, 65)} "
                    f"-t {float(rand.randrange(65, 90)/100)}"
                ),
                "file-edges",
                "minimum",
                True,
                False,
                False,
                True,
                True,
                False,
                False,
                True,
                False,
                "",
            ),
        ],
        "Random": [
            "Randomness in every arg!",
            (
                (
                    f"-a {rand.randrange(0, 360)} "
                    f"-c {(rand.randrange(50, 500, 25))} "
                    f"-u {float(rand.randrange(50, 100, 5) / 100)} "
                    f"-t {float(rand.randrange(10, 50, 5) / 100)} "
                    f"-r {rand.randrange(5, 75)} "
                ),
                misc_variables["int_func_options"][
                    rand.randrange(0, len(misc_variables["int_func_options"]) - 2)
                ],
                misc_variables["sort_func_options"][
                    rand.randrange(0, len(misc_variables["sort_func_options"]))
                ],
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                "",
            ),
        ],
        "Snap": [
            "You could not live with your own failure. And where did that bring you? Back to me.",
            (
                (
                    f"-r {rand.randrange(15,50,5)} "
                    f"-c {(rand.randrange(50, 250, 25))} "
                    f"-a {rand.randrange(0,180)} "
                ),
                "snap",
                "minimum",
                True,
                False,
                False,
                True,
                True,
                False,
                True,
                False,
                False,
                "",
            ),
        ],
        "Kims": [
            "Used by Kim Asendorf's original processing script",
            (
                f"-a 90 -u {float(rand.randrange(15, 85)/100)}",
                "threshold",
                misc_variables["sort_func_options"][
                    rand.randrange(0, len(misc_variables["sort_func_options"]))
                ],
                True,
                False,
                False,
                True,
                True,
                False,
                False,
                False,
                False,
                "",
            ),
        ],
    }

    print(
        f"Pixel sorting based on {'web hosted images.' if misc_variables['internet'] else 'local images'}\n"
        f"Most of the backend is sourced from https://github.com/satyarth/pixelsort"
        f"\nThe output image is {'uploaded to put.re after being sorted.' if misc_variables['internet'] else 'saved locally.'}\n"
        f"\nTo see any past runs, args used, and the result image, open 'output.txt'\n"
        f"{(35 * '--')}"
        f"\nThanks for using this program!\nPress any key to continue..."
        f"\n\n\nFor anyone who has used the script before: put.re's api is currently down."
        f"\nThis means the script cannot upload image urls, so I've temporarily"
        f"\ndisabled the deletion of previous image files until this is resolved."
        f"\nSorry about the mess. Hope fully they will fix soon."
    )
    input()
    clear()

    if misc_variables["internet"]:
        url_input = input(
            "Please input the URL of the image, the default image #, or the image path:\n(this might take a while depending the image resolution)\n"
        )
        if len(url_input) > 79:
            print("Image URL too long, uploading to put.re for a shorter URL...")
            img = ImgOpen(url_input, misc_variables["internet"])
            img.save("image.png")
            url_input, misc_variables["image_upload_failed"] = UploadImg("image.png")
            RemoveOld("image.png")
        url, url_given, url_random, random_url = ReadImageInput(
            url_input, misc_variables, misc_variables["internet"]
        )
    else:
        print("Internet not connected! Local image must be used.")
        url_input = input(
            "Please input the location of the local file (default image in images folder):\n"
        )
        url, url_given, url_random, random_url = ReadImageInput(
            url_input, misc_variables, misc_variables["internet"]
        )
    input_img = ImgOpen(url, misc_variables["internet"])

    width, height = input_img.size
    misc_variables["resolution_msg"] = f"Resolution: {width}x{height}"
    misc_variables["image_msg"] = (
        (
            f"[WARNING] No image url given, using {('random' if url_random else 'chosen')}"
            f" default image {(random_url if url_random else str(url_input))}"
        )
        if not url_given
        else "Using given image "
    )
    clear()

    # preset input
    print(f"{misc_variables['image_msg']}\n{misc_variables['resolution_msg']}")
    preset_q = input("\nDo you wish to apply a preset? (y/n)\n").lower()
    clear()
    if preset_q in ["y", "yes", "1"]:
        presets_list: list = []
        for i in presets:
            Append(presets_list, i)

        print(f"{misc_variables['resolution_msg']}\n")
        for i, j in enumerate(presets_list):
            print(f"{i+1}|{j} -- {presets[j][0]}")
        print("-Any preset ID from the database can be used.")

        preset_input = input("\nChoice: ").lower()

        if preset_input in list(map(str, range(1, len(presets_list) + 1))):
            for i, j in enumerate(presets_list):
                if str(i + 1) == preset_input:
                    preset_input = str(j)
            # if presets are applied, they take over args
            (
                arg_parse_input,
                int_func_input,
                sort_func_input,
                misc_variables["preset_true"],
                misc_variables["int_rand"],
                misc_variables["sort_rand"],
                misc_variables["int_chosen"],
                misc_variables["sort_chosen"],
                misc_variables["shuffled"],
                misc_variables["snapped"],
                misc_variables["file_sorted"],
                db_preset,
                file_link,
            ) = ReadPreset(preset_input, width, presets)
    else:
        misc_variables["preset_true"], db_preset, file_link, preset_input = (
            False,
            False,
            "False",
            "None",
        )
    clear()

    # int func, sort func & int msg, sort msg
    if not misc_variables["preset_true"]:
        # int func input
        print(f"{misc_variables['image_msg']}\n{misc_variables['resolution_msg']}")

        print("\nWhat interval function are you using?\nOptions (default is random):")
        for i, j in enumerate(misc_variables["int_func_options"]):
            print(f"-{i+1}|{j}")
        print("-11|random select")

        int_func_input = input("\nChoice: ").lower()

        if int_func_input in list(
            map(str, range(1, len(misc_variables["int_func_options"]) + 1))
        ):
            int_func_input, misc_variables["int_chosen"], misc_variables["int_rand"] = (
                misc_variables["int_func_options"][int(int_func_input) - 1],
                True,
                False,
            )
        elif int_func_input in ["11", "random select"]:
            int_func_input, misc_variables["int_chosen"], misc_variables["int_rand"] = (
                misc_variables["int_func_options"][rand.randint(0, 3)],
                True,
                True,
            )
        else:
            misc_variables["int_chosen"], int_func_input = (
                (True, int_func_input)
                if int_func_input in misc_variables["int_func_options"]
                else (False, "random")
            )
            misc_variables["int_rand"] = False
        misc_variables["shuffled"] = (
            True if int_func_input in ["shuffle-total", "shuffle-axis"] else False
        )
        misc_variables["snapped"] = True if int_func_input in ["snap"] else False
        misc_variables["file_sorted"] = (
            True if int_func_input in ["file", "file-edges"] else False
        )

        misc_variables["int_msg"] = (
            (
                "Interval function: "
                if not misc_variables["int_rand"]
                else "Interval function (randomly selected): "
            )
            + int_func_input
            if misc_variables["int_chosen"]
            else "Interval function: random (default)"
        )
        clear()

        # sort func input
        print(
            f"{misc_variables['image_msg']}\n{misc_variables['int_msg']}\n{misc_variables['resolution_msg']}"
        )
        print("\nWhat sorting function are you using?\nOptions (default is lightness):")
        for i, j in enumerate(misc_variables["sort_func_options"]):
            print(f"-{i+1}|{j}")
        print("-6|random select")

        sort_func_input = input("\nChoice: ").lower()

        if sort_func_input in list(
            map(str, range(1, len(misc_variables["sort_func_options"]) + 1))
        ):
            # if sort_func_input in ["1", "2", "3", "4", "5"]:
            sort_func_input = misc_variables["sort_func_options"][
                int(sort_func_input) - 1
            ]
            misc_variables["sort_chosen"] = True
            misc_variables["sort_rand"] = False
        elif sort_func_input in ["6", "random select"]:
            sort_func_input = misc_variables["sort_func_options"][rand.randint(0, 4)]
            misc_variables["sort_chosen"] = True
            misc_variables["sort_rand"] = True
        else:
            misc_variables["sort_chosen"], sort_func_input = (
                (True, sort_func_input)
                if sort_func_input in misc_variables["sort_func_options"]
                else (False, "lightness")
            )
            misc_variables["sort_rand"] = False

        misc_variables["sort_msg"] = (
            (
                "Sorting function: "
                if not misc_variables["sort_rand"]
                else "Sorting function (randomly selected): "
            )
            + sort_func_input
            if misc_variables["sort_chosen"]
            else "Sorting function: lightness (default)"
        )
        clear()

    # int func msg, sort func msg
    if misc_variables["preset_true"]:
        misc_variables["int_msg"] = (
            (
                "Interval function: "
                if not misc_variables["int_rand"]
                else "Interval function (randomly selected): "
            )
            + int_func_input
            if int_func_input in misc_variables["int_func_options"]
            else "Interval function: random (default)"
        )

        misc_variables["sort_msg"] = (
            (
                "Sorting function: "
                if not misc_variables["sort_rand"]
                else "Sorting function (randomly selected): "
            )
            + sort_func_input
            if sort_func_input in misc_variables["sort_func_options"]
            else "Sorting function: lightness (default)"
        )

    # hosting site
    if misc_variables["internet"]:
        output_image_path = "images/image.png"
        misc_variables["site_msg"] = "Uploading sorted image to put.re"
    else:
        print("Internet not connected! Image will be saved locally.\n")
        file_name = input(
            "Name of output file (leave empty for randomized name):\n(do not include the file extension, .png will always be used.)\n"
        )
        output_image_path = (IDGen(5) + ".png") if file_name in ["", " "] else file_name
        misc_variables[
            "site_msg"
        ] = f"Internet not connected, saving locally as {output_image_path}"
    clear()

    # args
    if not misc_variables["preset_true"]:
        needs_help = input("Do you need help with args? (y/n)\n")
        clear()
        if needs_help in ["y", "yes", "1"]:
            print(
                f"{misc_variables['image_msg']}\n{misc_variables['resolution_msg']}\n{misc_variables['int_msg']}\n{misc_variables['sort_msg']}\n{misc_variables['site_msg']}\n"
                f"\nWhat args will you be adding?\n"
                f'{("{:21}".format("Parameter"))}{("{:>6}".format("| Flag |"))}{("{:>12}".format("Description"))}\n'
                f'{("{:21}".format("---------------------"))}{("{:>6}".format("|------|"))}{("{:>12}".format("------------"))}\n'
                f'{("{:21}".format("Randomness"))}{("{:>6}".format("| -r   |"))}What percentage of intervals not to sort. 0 by default. Takes values from 0-100.\n'
                f'{("{:21}".format("Char. length"))}{("{:>6}".format("| -c   |"))}Characteristic length for the random width generator.\n{29 * " "}Used in mode random. Minimum 0, no max.\n'
                f'{("{:21}".format("Angle"))}{("{:>6}".format("| -a   |"))}Angle at which you\'re pixel sorting in degrees. 0 (horizontal) by default. Takes values from 0-360.\n'
                f'{("{:21}".format("Threshold (lower)"))}{("{:>6}".format("| -t   |"))}How dark must a pixel be to be considered as a \'border\' for sorting?\n{29 * " "}Takes values from 0-1. 0.25 by default. Used in edges and threshold modes.\n'
                f'{("{:21}".format("Threshold (upper)"))}{("{:>6}".format("| -u   |"))}How bright must a pixel be to be considered as a \'border\' for sorting?\n{29 * " "}Takes values from 0-1. 0.8 by default. Used in threshold mode.\n'
            )
        else:
            print(
                f"{misc_variables['image_msg']}\n{misc_variables['resolution_msg']}\n{misc_variables['int_msg']}\n{misc_variables['sort_msg']}\n{misc_variables['site_msg']}\n"
                f"\nWhat args will you be adding?\n"
                f'{("{:21}".format("Parameter"))}{("{:>6}".format("| Flag |"))}\n'
                f'{("{:21}".format("---------------------"))}{("{:>6}".format("|------|"))}\n'
                f'{("{:21}".format("Randomness"))}{("{:>6}".format("| -r   |"))}\n'
                f'{("{:21}".format("Char. length"))}{("{:>6}".format("| -c   |"))}\n'
                f'{("{:21}".format("Angle"))}{("{:>6}".format("| -a   |"))}\n'
                f'{("{:21}".format("Threshold (lower)"))}{("{:>6}".format("| -t   |"))}\n'
                f'{("{:21}".format("Threshold (upper)"))}{("{:>6}".format("| -u   |"))}\n'
            )
        arg_parse_input = input("\nArgs: ")
        clear()

    # arg parsing
    if arg_parse_input in ["", " ", None]:
        print("No args given!")
        arg_parse_input = ""

    args_full = (
        f" -l {url}"
        f" -i {int_func_input}"
        f" -s {sort_func_input}"
        f" -b {preset_input}"
        f" -p {str(misc_variables['preset_true'])}"
        f" -d {str(db_preset)}"
        f" -y {str(misc_variables['internet'])}"
        f"{f' -k file_link' if db_preset else ''}"
    )

    args_namespace = parse.parse_args(arg_parse_input.split())
    util_args_namespace = parse_util.parse_args(args_full.split())

    __args = {
        "bottom_threshold": args_namespace.bottom_threshold,
        "upper_threshold": args_namespace.upper_threshold,
        "clength": args_namespace.clength,
        "angle": args_namespace.angle,
        "randomness": args_namespace.randomness,
        "url": util_args_namespace.url,
        "int_function": util_args_namespace.int_function,
        "sorting_function": util_args_namespace.sorting_function,
        "presetname": util_args_namespace.presetname,
        "filelink": util_args_namespace.filelink,
        "dbpreset": util_args_namespace.dbpreset,
        "preset": (util_args_namespace.preset),
        "internet": (util_args_namespace.internet),
    }

    interval_function = ReadIntervalFunction(int_func_input)
    sorting_function = ReadSortingFunction(sort_func_input)

    print(
        f"{misc_variables['image_msg']}\n{misc_variables['resolution_msg']}\n"
        f"{('Preset: ' + preset_input if misc_variables['preset_true'] else 'No preset applied')}"
        f"\n{misc_variables['int_msg']}\n{misc_variables['sort_msg']}\n{misc_variables['site_msg']}"
    )

    print(f"Lower threshold: {__args['bottom_threshold']}") if int_func_input in [
        "threshold",
        "edges",
        "file-edges",
        "snap",
    ] else None
    print(f"Upper threshold: {__args['upper_threshold']}") if int_func_input in [
        "threshold"
    ] else None
    print(f"Characteristic length: {__args['clength']}") if int_func_input in [
        "random",
        "waves",
    ] else None
    print(f"Randomness: {__args['randomness']} %")
    print(f"Angle: {__args['angle']} °")
    print("------------------------------")

    print("Rotating image...")
    input_img = input_img.rotate(__args["angle"], expand=True)

    print("Getting data...")
    data = input_img.load()

    size0, size1 = input_img.size
    pixels = PixelAppend(size1, size0, data, "Getting pixels...")

    if (
        misc_variables["shuffled"]
        or misc_variables["snapped"]
        or __args["int_function"] in ["snap", "shuffle-total", "shuffle-axis"]
    ):
        if misc_variables["snapped"] or __args["int_function"] == "snap":
            intervals = file_edges(pixels, __args)
            sorted_pixels = SortImage(pixels, intervals, __args, sorting_function)
            print(
                f"{('/' * 45)}\n"
                f"Dread it. Run from it. Destiny still arrives."
                f"\n{('/' * 45)}"
            )
            thanos_img = Image.new("RGBA", input_img.size)
            size0, size1 = thanos_img.size
            for y in ProgressBars(size1, "The end is near..."):
                for x in range(size0):
                    ImgPixels(thanos_img, x, y, pixels)
            thanos_img.save("images/thanos_img.png")
            print("I am... inevitable...")
            sorted_pixels = interval_function(sorted_pixels, __args)
        else:
            sorted_pixels = interval_function(pixels, __args)
    else:
        intervals = interval_function(pixels, __args)
        sorted_pixels = SortImage(pixels, intervals, __args, sorting_function)

    output_img = Image.new("RGBA", input_img.size)
    size0, size1 = output_img.size
    for y in ProgressBars(size1, "Building output image..."):
        for x in range(size0):
            ImgPixels(output_img, x, y, sorted_pixels)

    if __args["angle"] is not 0:
        print("Rotating output image back to original orientation...")
        output_img = output_img.rotate(360 - __args["angle"], expand=True)

        print("Crop image to apropriate size...")
        output_img = CropTo(output_img, __args)

    print("Saving image...")
    output_img.save(output_image_path)
    output_img.show()

    if misc_variables["internet"]:
        print("Uploading...")
        misc_variables["link"], misc_variables["image_upload_failed"] = UploadImg(
            "images/image.png"
        )
        print("Image uploaded!")

        if misc_variables["file_sorted"] or (
            misc_variables["snapped"] and misc_variables["preset_true"]
        ):
            file_link, misc_variables["image_upload_failed"] = UploadImg(
                "images/ElementaryCA.png"
            )
            print("File image uploaded!")
        else:
            file_link = ""

        # delete old file, seeing as its uploaded as long as it didn't fail to upload
        if misc_variables["image_upload_failed"] == True:
            print("Removing local file...")
            RemoveOld(output_image_path)
            RemoveOld("images/ElementaryCA.png")

        # output to 'output.txt'
        print("Saving config to 'output.txt'...")
        with open("output.txt", "a") as f:
            f.write(
                f"\nStarting image url: {url}\n{misc_variables['resolution_msg']}\n"
                f'{("Int func: " if not misc_variables["int_rand"] else "Int func (randomly chosen): ")}{int_func_input}\n'
                f'{(("File link: ") + file_link) if misc_variables["file_sorted"] or misc_variables["snapped"] else ""}\n'
                f'{("Sort func: " if not misc_variables["sort_rand"] else "Sort func (randomly chosen): ")}{sort_func_input}\n'
                f'Args: {(arg_parse_input if arg_parse_input is not None else "No args")}\n'
                f'Sorted on: {misc_variables["date_time"]}\n\nSorted image: {misc_variables["link"]}\n{(35 * "-")}'
            )

        print("Uploading to DB...")
        dbURL = "https://pixelsorting-a289.restdb.io/rest/outputs"
        payload = dumps(
            {
                "start_link": f"{url}",
                "resolution": f"{misc_variables['resolution_msg'][11:]}",
                "int_func": f"{int_func_input}",
                "file_link": f"{file_link}",
                "sort_func": f"{sort_func_input}",
                "args": f"{arg_parse_input}",
                "date": f"{misc_variables['date_time']}",
                "sorted_link": f"{misc_variables['link']}",
                "preset_id": f"{misc_variables['preset_id']}",
            }
        )
        headers = {
            "content-type": "application/json",
            "x-apikey": "acc71784a255a80c2fd25e081890a1767edaf",
            "cache-control": "no-cache",
        }
        request("POST", dbURL, data=payload, headers=headers)

        print("Done!")
        print(f"Link to image: {misc_variables['link']}")
    else:
        print("Not saving config to 'output.txt', as there is no internet.\nDone!")


if __name__ == "__main__":
    main()
