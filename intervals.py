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

from MiscFuncs import PixelAppend, ElementaryCA
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
    lightness,
    intensity,
    hue,
    saturation,
    minimum,
)


def edge(pixels: Any, args: Any) -> List:
    edge_data: Any = (
        ImgOpen(args.url, args.internet)
        .rotate(args.angle, expand=True)
        .filter(ImageFilter.FIND_EDGES)
        .convert("RGBA")
        .load()
    )

    filter_pixels = PixelAppend(
        len(pixels), len(pixels[0]), edge_data, "Finding threshold..."
    )
    edge_pixels: List = []
    intervals: List = []

    for y in ProgressBars(len(pixels), "Thresholding..."):
        Append(edge_pixels, [])
        for x in range(len(pixels[0])):
            AppendBW(edge_pixels, x, y, filter_pixels, args.bottom_threshold)

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if (
                edge_pixels[y][x] == black_pixel
                and edge_pixels[y][x - 1] == black_pixel
            ):
                edge_pixels[y][x] = white_pixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == black_pixel:
                AppendPartial(intervals, y, x)
        AppendPartial(intervals, y, len(pixels[0]))
    return intervals


def threshold(pixels: Any, args: Any) -> List:
    intervals: List = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if (
                lightness(pixels[y][x]) < args.bottom_threshold
                or lightness(pixels[y][x]) > args.upper_threshold
            ):
                AppendPartial(intervals, y, x)
        AppendPartial(intervals, y, len(pixels[0]))
    return intervals


def random(pixels: Any, args: Any) -> List:
    intervals: List = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        x = 0
        while True:
            width = RandomWidth(args.clength)
            x += width
            if x > len(pixels[0]):
                AppendPartial(intervals, y, len(pixels[0]))
                break
            else:
                AppendPartial(intervals, y, x)
    return intervals


def waves(pixels: Any, args: Any) -> List:
    intervals: List = []

    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [])
        x = 0
        while True:
            width = args.clength + rand.randint(0, 10)
            x += width
            if x > len(pixels[0]):
                AppendPartial(intervals, y, len(pixels[0]))
                break
            else:
                AppendPartial(intervals, y, x)
    return intervals


def file_mask(pixels: Any, args: Any) -> List:
    img = ElementaryCA(pixels).resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
    data: Any = img.load()

    file_pixels = PixelAppend(img.size[1], img.size[0], data, "Defining edges...")
    intervals: List = []

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up edges..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if (
                file_pixels[y][x] == black_pixel
                and file_pixels[y][x - 1] == black_pixel
            ):
                file_pixels[y][x] = white_pixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if file_pixels[y][x] == black_pixel:
                AppendPartial(intervals, y, x)
        AppendPartial(intervals, y, len(pixels[0]))

    return intervals


def file_edges(pixels: Any, args: Any) -> List:
    edge_data: Any = (
        ElementaryCA(pixels)
        .rotate(args.angle, expand=True)
        .resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
        .filter(ImageFilter.FIND_EDGES)
        .convert("RGBA")
        .load()
    )

    filter_pixels = PixelAppend(
        len(pixels), len(pixels[0]), edge_data, "Defining edges..."
    )
    edge_pixels: List = []
    intervals: List = []

    for y in ProgressBars(len(pixels), "Thresholding..."):
        Append(edge_pixels, [])
        for x in range(len(pixels[0])):
            AppendBW(edge_pixels, x, y, filter_pixels, args.bottom_threshold)

    for y in tqdm(
        range(len(pixels) - 1, 1, -1), desc=("{:30}".format("Cleaning up edges..."))
    ):
        for x in range(len(pixels[0]) - 1, 1, -1):
            if (
                edge_pixels[y][x] == black_pixel
                and edge_pixels[y][x - 1] == black_pixel
            ):
                edge_pixels[y][x] = white_pixel

    for y in ProgressBars(len(pixels), "Defining intervals..."):
        Append(intervals, [])
        for x in range(len(pixels[0])):
            if edge_pixels[y][x] == black_pixel:
                AppendPartial(intervals, y, x)
        AppendPartial(intervals, y, len(pixels[0]))
    return intervals


def snap_sort(pixels: Any, args: Any) -> List:
    input_img = ImgOpen("images/thanos_img.png", False)
    pixels_snap: Any = np.asarray(input_img)

    print("The hardest choices require the strongest wills...")
    nx, ny = input_img.size
    xy: Any = np.mgrid[:nx, :ny].reshape(2, -1).T
    rounded: int = int(round(int(xy.shape[0] / 2), 0))

    numbers_that_dont_feel_so_good: Any = xy.take(
        np.random.choice(xy.shape[0], rounded, replace=False), axis=0
    )
    print(f'Number of those worthy of the sacrifice: {("{:,}".format(rounded))}')

    pixels_snap.setflags(write=1)
    for i in ProgressBars(len(numbers_that_dont_feel_so_good), "Snapping..."):
        pixels_snap[numbers_that_dont_feel_so_good[i][1]][
            numbers_that_dont_feel_so_good[i][0]
        ] = [0, 0, 0, 0]

    print("Sorted perfectly in half.")
    feel_better: Any = Image.fromarray(pixels_snap, "RGBA")
    feel_better.save("images/snapped_pixels.png")

    snapped_img = ImgOpen("images/snapped_pixels.png", False)
    data: Any = snapped_img.load()
    size0, size1 = snapped_img.size
    pixels_return = PixelAppend(size1, size0, data, "I hope they remember you...")

    os.remove("images/snapped_pixels.png")
    os.remove("images/thanos_img.png")
    print(f"{('/' * 45)}\nPerfectly balanced, as all things should be.\n{('/' * 45)}")

    return pixels_return


def shuffle_total(pixels: Any, args: Any) -> List:
    print("Creating array from image...")
    input_img = ImgOpen(args.url, args.internet)
    height: int = input_img.size[1]
    shuffle: Any = np.array(input_img)

    for i in ProgressBars(int(height), "Shuffling image..."):
        np.random.shuffle(shuffle[i])
    shuffled_out: Any = Image.fromarray(shuffle, "RGB")
    shuffled_out.save("images/shuffled.png")
    shuffled_img = ImgOpen("images/shuffled.png", False)
    data: Any = shuffled_img.load()

    size0, size1 = input_img.size
    pixels = PixelAppend(size1, size0, data, "Recreating image...")

    os.remove("images/shuffled.png")
    return pixels


def shuffled_axis(pixels: Any, args: Any) -> List:
    print("Creating array from image...")
    input_img = ImgOpen(args.url, args.internet)
    height: int = input_img.size[1]
    shuffle: Any = np.array(input_img)

    for _ in ProgressBars(height, "Shuffling image..."):
        np.random.shuffle(shuffle)
    shuffled_out: Any = Image.fromarray(shuffle, "RGB")
    shuffled_out.save("images/shuffled.png")
    shuffled_img = ImgOpen("images/shuffled.png", False)
    data: Any = shuffled_img.load()

    size0, size1 = input_img.size
    pixels = PixelAppend(size1, size0, data, "Recreating image...")

    os.remove("images/shuffled.png")
    return pixels


def none(pixels: Any, args: Any) -> List:
    intervals: List = []
    for y in ProgressBars(len(pixels), "Determining intervals..."):
        Append(intervals, [len(pixels[y])])
    return intervals
