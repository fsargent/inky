# a programme to display today's weather and tomorrow
# on the inky_display using Lukas Kubis's Python wrapper
# for the Dark Sky API https://github.com/lukaskubis/darkskylib

import glob
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import datetime
from datetime import date, timedelta
import textwrap

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.RED)

def drawInky(today, tomorrow):
    # w.detailed_status         # 'clouds'
    # w.wind()                  # {'speed': 4.6, 'deg': 330}
    # w.humidity                # 87
    # w.temperature('celsius')  # {'max': 10.5, 'day': 9.7, 'min': 9.0}
    # w.rain                    # {}
    # w.heat_index              # None
    # w.clouds                  # 75

    # # Will it be clear tomorrow at this time in Milan (Italy) ?
    # forecast = mgr.forecast_at_place('Milan,IT', 'daily')
    # answer = forecast.will_be_clear_at(timestamps.tomorrow())

    # Create a new blank image, img, of type P
    # that is the width and height of the Inky pHAT display,
    # then create a drawing canvas, draw, to which we can draw text and graphics
    img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # import the fonts and set sizes
    tempFont = ImageFont.truetype('fonts/Aller_Bd.ttf', 22)
    dayFont = ImageFont.truetype('fonts/Roboto-Black.ttf', 18)
    dateFont = ImageFont.truetype('fonts/Roboto-Bold.ttf', 14)
    font = ImageFont.truetype('fonts/ElecSign.ttf', 10)
    smallFont = ImageFont.truetype('fonts/ElecSign.ttf', 8)
    smallestFont = ImageFont.truetype('fonts/ElecSign.ttf', 7)


    # define weekday text
    weekday = date.today()
    day_Name = date.strftime(weekday, '%A')
    day_month_year = date.strftime(weekday, '%-d %B %y')

    weekday2 = datetime.date.today() + datetime.timedelta(days=1)
    day2 = date.strftime(weekday2, '%A')

    # format the summary texts for today and tomorrow
    currentCondFormatted = textwrap.fill(today.detailed_status, 16)
    summary2Formatted = textwrap.fill(today.detailed_status, 18)

    # draw some lines to box out tomorrow's forecast
    draw.line((118, 50, 118, 104),2, 4)
    draw.line((118, 50, 212, 50),2, 4)

    # draw today's name on top left side
    draw.text((3, 3), day_Name, inky_display.BLACK, dayFont)

    # draw today's date on left side below today's name
    dayDate = day_month_year
    draw.text((3, 25), dayDate, inky_display.BLACK, dateFont)

    #draw current temperature to right of day name and date
    draw.text((105, 8), '{0:.0f}'.format(today.temperature('celsius')['day']) + '°', inky_display.BLACK, tempFont)
    draw.text((105, 34), str(today.temperature('fahrenheit')['day']) + 'F', inky_display.BLACK, font)

    # draw today's high and low temps to center on left side below date
    w, h = dateFont.getsize(str(today.temperature('fahrenheit')['min']) + str(today.temperature('fahrenheit')['max']))
    x_temps = (inky_display.WIDTH / 4) - (w / 2)
    tempsToday = 'High ' + '{0:.0f}'.format(today.temperature('fahrenheit')['max']) + ' Low ' + '{0:.0f}'.format(today.temperature('fahrenheit')['min'])
    draw.text((x_temps, 45), tempsToday, inky_display.BLACK, font)

    # draw the current summary and conditions on the left side of the screen
    draw.text((3, 60), currentCondFormatted, inky_display.BLACK, smallFont)



    # draw tomorrow's forecast in lower right box
    draw.text((125, 55), day2, inky_display.BLACK, font)
    draw.text((125, 66), '{0:.0f}'.format(tomorrow.temperature('celsius')['day']) + '°', inky_display.BLACK, smallFont)
    draw.text((125, 77), tomorrow.detailed_status, inky_display.BLACK, smallestFont)

    # prepare to draw the icon on the upper right side of the screen
    # Dictionary to store the icons
    icons = {}

    # build the dictionary 'icons'
    for icon in glob.glob('weather-icons/*.png'):
        # format the file name down to the text we need
        # example: 'icon-fog.png' becomes 'fog'
        # and gets put in the libary
        icon_name = icon.replace('.png', '')
        icon_image = Image.open(icon)
        icons[icon_name] = icon_image


    # Draw the current weather icon top in top right
    if today.weather_icon_name is not None:
        img.paste(icons[today.weather_icon_name], (145, 2))
    else:
        draw.text((140, 10), '?', inky_display.RED, dayFont)


    # set up the image to push it
    inky_display.set_image(img)
    inky_display.set_border(inky_display.RED)

    # push it all to the screen
    inky_display.show()