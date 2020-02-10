from random import choice, shuffle

from util import *
from pixelsort import ElementaryCA

from tqdm import tqdm
from PIL import Image, ImageFilter
from numpy import array, mgrid


# INTERVALS #
def edge(pixels, args) -> List:
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


def threshold(pixels, args) -> List:
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


def random(pixels, args) -> List:
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


def waves(pixels, args) -> List:
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


def file_mask(pixels, args) -> List:
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


def file_edges(pixels, args) -> List:
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


def snap_sort(pixels, args) -> List:
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


def shuffle_total(pixels, args) -> List:
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


def shuffled_axis(pixels, args) -> List:
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


def none(pixels, args) -> List:
    intervals = []
    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [len(pixels[y])])
    return intervals
