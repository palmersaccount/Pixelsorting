try:
    from PIL import Image
except ImportError:
    from PIL import Image, ImageFilter
import os
import numpy as np
import random as rand
import util
import requests

black_pixel = (0, 0, 0, 255)
white_pixel = (255, 255, 255, 255)


def edge(pixels, args, url):
    img = Image.open(requests.get(url, stream=True).raw)
    img = img.rotate(args.angle, expand=True)
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    appendF = filter_pixels.append
    edge_pixels = []
    appendE = edge_pixels.append
    intervals = []
    appendInt = intervals.append

    size1 = img.size[1]
    size0 = img.size[0]

    print("Defining edges...")
    for y in range(size1):
        appendF([])
        for x in range(size0):
            filter_pixels[y].append(edge_data[x, y])

    print("Thresholding...")
    for y in range(len(pixels)):
        appendE([])
        for x in range(len(pixels[0])):
            if util.lightness(filter_pixels[y][x]) < args.bottom_threshold:
                edge_pixels[y].append(white_pixel)
            else:
                edge_pixels[y].append(black_pixel)

    print("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if edge_pixels[y][x] == black_pixel and edge_pixels[y][x - 1] == black_pixel:
                edge_pixels[y][x] = white_pixel

    print("Defining intervals...")
    for y in range(len(pixels)):
        appendInt([])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[0]))
    return intervals


def threshold(pixels, args, url):
    intervals = []
    appendInt = intervals.append

    print("Defining intervals...")
    for y in range(len(pixels)):
        appendInt([])
        for x in range(len(pixels[0])):
            if util.lightness(pixels[y][x]) < args.bottom_threshold or util.lightness(pixels[y][x]) > args.upper_threshold:
                intervals[y].append(x)
        intervals[y].append(len(pixels[0]))
    return intervals


def random(pixels, args, url):
    intervals = []
    appendInt = intervals.append

    print("Defining intervals...")
    for y in range(len(pixels)):
        appendInt([])
        x = 0
        while True:
            width = util.random_width(args.clength)
            x += width
            if x > len(pixels[0]):
                intervals[y].append(len(pixels[0]))
                break
            else:
                intervals[y].append(x)
    return intervals


def waves(pixels, args, url):
    intervals = []
    appendInt = intervals.append

    print("Defining intervals...")
    for y in range(len(pixels)):
        appendInt([])
        x = 0
        while True:
            width = args.clength + rand.randint(0, 10)
            x += width
            if x > len(pixels[0]):
                intervals[y].append(len(pixels[0]))
                break
            else:
                intervals[y].append(x)
    return intervals


def file_mask(pixels, args, url):
    intervals = []
    file_pixels = []

    int_file = input(
        "Please enter the URL of an int file or hit enter to randomly select one:\n")
    img = Image.open(requests.get(int_file, stream=True).raw)
    img = img.convert('RGBA')
    img = img.rotate(args.angle, expand=True)
    data = img.load()
    for y in range(img.size[1]):
        file_pixels.append([])
        for x in range(img.size[0]):
            file_pixels[y].append(data[x, y])

    print("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if file_pixels[y][x] == black_pixel and file_pixels[y][x - 1] == black_pixel:
                file_pixels[y][x] = white_pixel

    print("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[0])):
            if file_pixels[y][x] == black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[0]))

    return intervals


def file_edges(pixels, args, url):
    int_file = input("Please enter the URL of an int file:\n")
    img = Image.open(requests.get(int_file, stream=True).raw)
    img = img.rotate(args.angle, expand=True)
    img = img.resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    edge_pixels = []
    intervals = []

    print("Defining edges...")
    for y in range(img.size[1]):
        filter_pixels.append([])
        for x in range(img.size[0]):
            filter_pixels[y].append(edge_data[x, y])

    print("Thresholding...")
    for y in range(len(pixels)):
        edge_pixels.append([])
        for x in range(len(pixels[0])):
            if util.lightness(filter_pixels[y][x]) < args.bottom_threshold:
                edge_pixels[y].append(white_pixel)
            else:
                edge_pixels[y].append(black_pixel)

    print("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if edge_pixels[y][x] == black_pixel and edge_pixels[y][x - 1] == black_pixel:
                edge_pixels[y][x] = white_pixel

    print("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[0]))
    return intervals


def snap_sort(pixels, args, url):
    print("Gaining power...")
    input_img = Image.open(requests.get(url, stream=True).raw)
    input_img = input_img.convert("RGBA")
    width, height = input_img.size
    print("Opening the soul stone...")
    pixels = np.asarray(input_img)

    print("Balancing perfectly...")
    nx, ny = height, width
    xy = np.mgrid[:nx, :ny].reshape(2, -1).T
    numbers_that_dont_feel_so_good = xy.take(np.random.choice(xy.shape[0], round(int(xy.shape[0] / 2), 0), replace=False), axis=0)
    
    pixels.setflags(write=1)
    for i in range(round(int(xy.shape[0] / 2), 0)):
        pixels[numbers_that_dont_feel_so_good[i][0]][numbers_that_dont_feel_so_good[i][1]] = [255, 255, 255, 0]

    print("Perfectly balanced, as all things should be.")
    feel_better = Image.fromarray(pixels, 'RGBA')
    feel_better.save("pixels_that_dont_feel_so_good.png")
    
    print("Allowing the saved to return...")
    input_img = Image.open("pixels_that_dont_feel_so_good.png")
    input_img = input_img.convert("RGBA")
    data = input_img.load()
    pixels = []
    append = pixels.append
    size1 = input_img.size[1]
    size0 = input_img.size[0]

    for y in range(size1):
        append([])
        for x in range(size0):
            pixels[y].append(data[x, y])
    print("Removing dust from the snap...")
    os.remove("pixels_that_dont_feel_so_good.png")
    print("Sorted perfectly in half.")
    
    return pixels


def shuffle_total(pixels, args, url):
    print("Creating array from image...")
    input_img = Image.open(requests.get(url, stream=True).raw)
    height = input_img.size[1]
    shuffle = np.array(input_img)

    print("Shuffling image...")
    for i in range(int(height)):
        np.random.shuffle(shuffle[i])
    shuffled_out = Image.fromarray(shuffle, 'RGB')
    shuffled_out.save("shuffled_total.png")
    shuffled_img = Image.open("shuffled_total.png")
    data = shuffled_img.load()

    pixels = []
    append = pixels.append
    size1 = shuffled_img.size[1]
    size0 = shuffled_img.size[0]

    print("Recreating image from array...")
    for y in range(size1):
        append([])
        for x in range(size0):
            pixels[y].append(data[x, y])

    os.remove("shuffled_total.png")
    return pixels


def shuffled_axis(pixels, args, url):
    print("Getting image...")
    input_img = Image.open(requests.get(url, stream=True).raw)
    height = input_img.size[1]
    shuffle = np.array(input_img)

    print("Shuffling image...")
    for i in range(int(height)):
        np.random.shuffle(shuffle)
    shuffled_out = Image.fromarray(shuffle, 'RGB')
    shuffled_out.save("shuffled_axis.png")
    shuffled_img = Image.open("shuffled_axis.png")
    data = shuffled_img.load()
    pixels = []
    append = pixels.append
    size1 = shuffled_img.size[1]
    size0 = shuffled_img.size[0]

    print("Recreating image from array...")
    for y in range(size1):
        append([])
        for x in range(size0):
            pixels[y].append(data[x, y])
    os.remove("shuffled_axis.png")
    return pixels


def none(pixels, args, url):
    intervals = []
    appendInt = intervals.append
    for y in range(len(pixels)):
        appendInt([len(pixels[y])])
    return intervals
