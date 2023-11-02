import webcolors
from typing import Tuple


def closest_color(requested_color: Tuple[int, int, int]) -> str:
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def hex_to_name(hex_color):
    try:
        rgb_color = webcolors.hex_to_rgb(hex_color)
        return webcolors.rgb_to_name(rgb_color)
    except ValueError:
        return closest_color(rgb_color)


# print(hex_to_name("#FFCE30"))
