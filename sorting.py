from colorsys import rgb_to_hsv

# SORTING PIXELS #
lightness = lambda p: rgb_to_hsv(p[0], p[1], p[2])[2] / 255.0
intensity = lambda p: p[0] + p[1] + p[2]
hue = lambda p: rgb_to_hsv(p[0], p[1], p[2])[0] / 255.0
saturation = lambda p: rgb_to_hsv(p[0], p[1], p[2])[1] / 255.0
minimum = lambda p: min(p[0], p[1], p[2])

