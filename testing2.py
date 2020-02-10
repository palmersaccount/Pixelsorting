"""
import logging
import argparse

p = argparse.ArgumentParser()

logging_level = 0

print(f"level: {logging_level}")

logging.basicConfig(
    format="%(levelname)s - %(message)s", level=logging.getLevelName(logging_level),
)

logging.debug("test")
logging.debug("\ntest2")
"""

from requests import request, get, post
from json import dumps, dump, loads, load


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
        return link
    except FileNotFoundError:
        print(f"{'---'*15}\n'{img}' not usable!\n{'---'*15}")
    except KeyError:
        print(f"{'---'*15}\n{output['message']}\n{'---'*15}")


link = UploadImg("images/default.jpg")
