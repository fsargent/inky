#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
from sys import exit

from font_fredoka_one import FredokaOne
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

# Get the current path
PATH = os.path.dirname(__file__)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.BLACK)

WARNING_TEMP = 25.0


def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    """Create a transparency mask.

    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.

    :param mask: Optional list of Inky pHAT colours to allow.

    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image


def drawInky(temperature, pressure, summary):
	# Dictionaries to store our icons and icon masks in
	icons = {}
	masks = {}

	# This maps the weather summary from Dark Sky
	# to the appropriate weather icons
	icon_map = {
			"snow": ["snow"],
			"rain": ["rain"],
			"cloud": ['scattered clouds','broken clouds', 'mist'],
			"sun": ["clear sky", "few clouds"],
			"storm": ['thunderstorm'],
			"wind": ["wind"]}


	for icon in icon_map:
			if summary in icon_map[icon]:
					weather_icon = icon
					break

	# Create a new canvas to draw on
	img = Image.open(os.path.join(PATH, "resources/backdrop.png")).resize(inky_display.resolution)
	draw = ImageDraw.Draw(img)

	# Load our icon files and generate masks
	for icon in glob.glob(os.path.join(PATH, "resources/icon-*.png")):
			icon_name = icon.split("icon-")[1].replace(".png", "")
			icon_image = Image.open(icon)
			icons[icon_name] = icon_image
			masks[icon_name] = create_mask(icon_image)

	# Load the FredokaOne font
	font = ImageFont.truetype(FredokaOne, 22)

	# Draw lines to frame the weather data
	draw.line((69, 36, 69, 81))       # Vertical line
	draw.line((31, 35, 184, 35))      # Horizontal top line
	draw.line((69, 58, 174, 58))      # Horizontal middle line
	draw.line((169, 58, 169, 58), 2)  # Red seaweed pixel :D

	# Write text with weather values to the canvas
	datetime = time.strftime("%d/%m %H:%M")

	draw.text((36, 12), datetime, inky_display.WHITE, font=font)

	draw.text((72, 34), "T", inky_display.WHITE, font=font)
	draw.text((92, 34), u"{}°".format(temperature), inky_display.WHITE if temperature < WARNING_TEMP else inky_display.RED, font=font)

	draw.text((72, 58), "P", inky_display.WHITE, font=font)
	draw.text((92, 58), "{}".format(pressure), inky_display.WHITE, font=font)

	# Draw the current weather icon over the backdrop
	if weather_icon is not None:
			img.paste(icons[weather_icon], (28, 36), masks[weather_icon])

	else:
			draw.text((28, 36), "?", inky_display.RED, font=font)

	# Display the weather data on Inky pHAT
	inky_display.set_image(img)
	inky_display.show()

