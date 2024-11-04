import colorsys
import json
import os
from colortones._structure._phonetics._inflections import *


def _RGB_to_HSV(rgb):
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (int(h * 255), int(s * 255), int(v * 255))


def _interpolate_RGB(left_rgb, right_rgb, interpolation=0.5):
    """Returns the RGB value that's somewhere between two colors."""
    diff = tuple(r - l for r, l in zip(right_rgb, left_rgb))
    return tuple(int(l + d * interpolation) for l, d in zip(left_rgb, diff))


def _RGB_to_hex(rgb):
    """Returns the given RGB as a hex value."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _determine_color_embedding(rgb):
    OPTIONS = {
        (197, 15, 31): "\033[31m",  # red
        (19, 161, 14): "\033[32m",  # green
        (193, 156, 0): "\033[33m",  # yellow
        (0, 44, 173): "\033[34m",  # blue
        (136, 23, 152): "\033[35m",  # purple
        (0, 138, 113): "\033[36m",  # cyan
        (255, 255, 255): "\033[37m",  # white
        (113, 113, 113): "\033[90m",  # gray
    }

    options_hsv_to_rgb = {}
    for key in OPTIONS.keys():
        hsv_key = _RGB_to_HSV(key)
        options_hsv_to_rgb[hsv_key] = key

    def euclidean_distance(color1, color2):
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

    hsv = _RGB_to_HSV(rgb)
    closest_hsv = min(
        options_hsv_to_rgb.keys(),
        key=lambda color: euclidean_distance(hsv, color),
    )
    closest_color = options_hsv_to_rgb[closest_hsv]
    return OPTIONS[closest_color]


def load_color_scheme(
    scheme_name: str,
    neutral_interpolation=0.5,
    rising_low_interpolation=0.5,
):
    """
    Returns a dictionary that binds each inflection value
    to a tuple that contains an RGB color, a HEX conversion,
    and an escape code for showing the color in the console.

    Parameters:
    scheme_name (str): name of the color scheme in _schemes.json to be used.
    neutral_interpolation (num): 0.0 will make all inflected neutrals
                                 be the neutral color.
                                 1.0 will make all inflected neutrals
                                 match their preceding inflections exactly.
    rising_low_interpolation (num): 0.0 will make rising lows the low color.
                                    1.0 will make rising lows the rising color.

    Returns:
    dict: binds each inflection value to a tuple
          that contains an RGB color and a HEX conversion.
    """
    FALLBACK = {
        "high-color": [255, 157, 18],
        "rising-color": [0, 190, 36],
        "low-color": [0, 87, 190],
        "falling-color": [176, 111, 219],
        "neutral-color": [128, 128, 128],
    }

    """
    Step 1) Attempts to load the dictionary of all color schemes.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemes_path = os.path.join(current_dir, "_schemes.json")
    if not os.path.exists(schemes_path):
        # defaults if the schemes file can't be found.
        print(f"Could not find the color schemes file at {schemes_path}")
        scheme = FALLBACK
    else:
        # loads the contents of the file as a dictionary.
        with open(schemes_path, "r") as file:
            all_schemes = json.load(file)

        scheme = all_schemes.get(scheme_name.lower())
        if scheme is None:
            msg = "Could not find the color scheme named"
            print(f'{msg} "{scheme_name}" in {schemes_path}')
            scheme = all_schemes.get("default")
            if scheme is None:
                print("No standard scheme was found either.")
                scheme = FALLBACK

    """
    Step 2) Extrapolates colors for every inflection from the color scheme.
    """
    scheme = {key: tuple(value) for key, value in scheme.items()}  # -> tuples.
    scheme["fallback-color"] = (255, 255, 255)
    high = scheme["high-color"]
    rising = scheme["rising-color"]
    low = scheme["low-color"]
    falling = scheme["falling-color"]
    neutral = scheme["neutral-color"]
    n_high = _interpolate_RGB(neutral, high, neutral_interpolation)
    n_rising = _interpolate_RGB(neutral, rising, neutral_interpolation)
    n_low = _interpolate_RGB(neutral, low, neutral_interpolation)
    n_falling = _interpolate_RGB(neutral, falling, neutral_interpolation)
    rising_low = _interpolate_RGB(low, rising, rising_low_interpolation)
    result = {
        PUNCTUATION_INFLECTION: scheme["fallback-color"],
        HIGH_INFLECTION: high,
        RISING_INFLECTION: rising,
        LOW_INFLECTION: low,
        FALLING_INFLECTION: falling,
        NEUTRAL_INFLECTION: neutral,
        FULL_LOW_INFLECTION: low,
        HALF_FALLING_INFLECTION: falling,
        NEUTRAL_HIGH_INFLECTION: n_high,
        NEUTRAL_RISING_INFLECTION: n_rising,
        NEUTRAL_LOW_INFLECTION: n_low,
        NEUTRAL_FALLING_INFLECTION: n_falling,
        RISING_LOW_INFLECTION: rising_low,
        RISING_YI_INFLECTION: rising,
        FALLING_YI_INFLECTION: falling,
        RISING_BU_INFLECTION: rising,
    }

    """
    Step 3) Adds the hex and escape ANSI to each entry.
    """
    for key, value in result.items():
        result[key] = (
            value,
            _RGB_to_hex(value),
            (
                _determine_color_embedding(value)
                if not inflection_is_neutral(key)
                else "\033[90m"
            ),
        )

    return result
