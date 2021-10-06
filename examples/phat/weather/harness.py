#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
from sys import exit

"""
To run this example on Python 2.x you should:
    sudo apt install python-lxml
    sudo pip install geocoder requests font-fredoka-one beautifulsoup4=4.6.3

On Python 3.x:
    sudo apt install python3-lxml
    sudo pip3 install geocoder requests font-fredoka-one beautifulsoup4
"""
print("""Inky pHAT: Weather

Displays weather information for a given location.
""")


from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config_for_subscription_type
config_dict = get_default_config_for_subscription_type('free')
owm = OWM('309fb812c9488f4eb0cf0eaa857567eb',config_dict)
mgr = owm.weather_manager()
observation = mgr.one_call(lat=37.76783042803676, lon=-122.42537156211634)
w = observation.forecast_daily[0]
t = observation.forecast_daily[1]

# w.detailed_status         # 'clouds'
# w.wind()                  # {'speed': 4.6, 'deg': 330}
# w.humidity                # 87
# w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
# w.rain                    # {}
# w.heat_index              # None
# w.clouds                  # 75

# # Will it be clear tomorrow at this time in Milan (Italy) ?
# forecast = mgr.forecast_at_place('Milan,IT', 'daily')
# answer = forecast.will_be_clear_at(timestamps.tomorrow())

if os.uname().machine == 'armv6l':
    from phatWeather2 import drawInky
    drawInky(w, t)

else:
    print(w.temperature('fahrenheit')['temp'], w.pressure['press'], w.detailed_status)
