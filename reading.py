from PIL import Image
import random
import requests

import interval
import sorting


def read_image_input(url_input, internet):
    # return order: url, url_given, url_random, random_url
    try:
        if internet:
            url = url_input
            Image.open(requests.get(url, stream=True).raw)
            return url, True, False, None
        else:
            if url_input in ['', ' ']:
                url = "images/default.jpg"
            else:
                url = url_input
            return url, True, False, False
    except IOError:
        random_url = str(random.randint(0, 5))
        url_options = {
            '0': "https://i.imgur.com/1UBT6fK.png",
            '1': "https://i.imgur.com/5VqeP6Y.jpg?1",
            '2': "https://i.imgur.com/rfasPI6.jpg?1",
            '3': "https://i.imgur.com/wFzJ6ua.jpg?1",
            '4': "https://i.imgur.com/pZRkMzP.jpg?1",
            '5': "https://i.imgur.com/HwchiaD.jpg?1",
            '6': "https://i.imgur.com/Z438D1L.jpg"
        }
        try:
            return ((url_options[(url_input if url_input in ['0', '1', '2', '3', '4', '5', '6'] else random_url)] if url_input in ['', ' ', '0', '1', '2', '3', '4', '5', '6'] else url_input),
                    (False if url_input in [
                     '', ' ', '0', '1', '2', '3', '4', '5', '6'] else True),
                    (True if url_input in ['', ' '] else False),
                    (random_url if url_input in ['', ' '] else None))
        except KeyError:
            return url_options[random_url], False, True, random_url


def read_interval_function(int_func_input):
    try:
        return {
            "random": interval.random,
            "threshold": interval.threshold,
            "edges": interval.edge,
            "waves": interval.waves,
            "snap": interval.snap_sort,
            "file": interval.file_mask,
            "file-edges": interval.file_edges,
            "shuffle-total": interval.shuffle_total,
            "shuffle-axis": interval.shuffled_axis,
            "none": interval.none,
        }[int_func_input]
    except KeyError:
        return interval.random


def read_sorting_function(sort_func_input):
    try:
        return {
            "lightness": sorting.lightness,
            "hue": sorting.hue,
            "intensity": sorting.intensity,
            "minimum": sorting.minimum,
            "saturation": sorting.saturation,
        }[sort_func_input]
    except KeyError:
        return sorting.lightness


def read_preset(preset_input):
    try:
        #order-- arg_parse_input, int_func_input, sort_func_input, preset_true, int_rand, sort_rand, shuffled, snapped
        int_func_input = {
            '1': 'random',
            '2': 'threshold',
            '3': 'edges',
            '4': 'waves'}
        sort_func_input = {
            '1': 'lightness',
            '2': 'hue',
            '3': 'intensity',
            '4': 'minimum',
            '5': 'saturation'}
        return {
            "main": (("-r 50 -c 250 -a 45"), "random", "intensity", True, False, False, False, False),
            "full random": (("-a "+str(random.randrange(0, 360))+" -c "+str(random.randrange(50, 500, 15))+" -u "+str((random.randrange(50, 100, 5)/100))+" -t "+str((random.randrange(5, 50, 5)/100))+" -r "+str(random.randrange(5, 100, 5))), int_func_input[str(random.randint(1, 4))], sort_func_input[str(random.randint(1, 5))], True, True, True, False, False),
            "snap-sort": (("-r 50 -c 250 -a 45"), "snap", "intensity", True, False, False, False, True)
        }[preset_input]
    except KeyError:
        print("[WARNING] Invalid preset name, no preset will be applied")
        return None, None, None, False, None, None, False, False


def read_site(site_input):
    try:
        return {
            "put.re": "put.re",
            "imgur": "imgur"
        }[site_input]
    except KeyError:
        return "put.re"
