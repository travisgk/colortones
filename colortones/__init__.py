"""
Filename: _init.py
Description: This is the main file for colortones.

Author: TravisGK
Version: 1.0

License: GNU License
"""

import json
import os
from ._structure._paragraph import Paragraph
from ._themes._color_scheme import load_color_scheme


def process_text(text_str: str):
    text_str = text_str.replace("\n", " ")
    text_str = text_str.strip()
    return Paragraph(text_str)
