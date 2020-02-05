"""
PLEASE IGNORE EVERYTHING IN THIS FILE

the idea is:
sample of 50 random permutations of a preset generator, merged together
"""


import os


def clear():
    return os.system("cls" if os.name == "nt" else "clear")


sort_func_options: list = ["lightness", "hue", "intensity", "minimum", "saturation"]
int_func_options: list = [
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
]


# for big sampling
import random
from itertools import permutations

sample_int_func: list = random.sample(list(permutations(range(8), 5)), 50)
# sample2_of_presets: list = random.sample(sample1_of_presets, 50)
total_iters: int = 0
total_partial_iters: int = 0

clear()

for i, j in enumerate(sample_int_func):
    if i % 2:
        print(f"{j[0]}")
        total_partial_iters += 1
    else:
        pass
    total_iters += 1

print(
    f"\ntotal: {total_iters}\ntotal partial: {total_partial_iters}\ntotal permutations: {len(sample_int_func)}"
)
# print(sample_of_presets)
