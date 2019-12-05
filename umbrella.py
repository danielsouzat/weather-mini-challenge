"""
@title:: Umbrella 1.0
@description: Get weather forecast data from openweathermap.com and tells for the week which days you should take an
umbrella when you leave home.
@author: Daniel de Souza Telles
@email: danieldesouzatelles@gmail.com
"""

import os
import requests
import time

# script configuration
api_key = "7dba2d39c8ecde4bcb88baf0074dd099"
city = "Ribeirão Preto"
country = "BR"

# set timezone to 'Brazil/East' so forecast is coherent with city local time in any computer
os.environ['TZ'] = 'Brazil/East'
time.tzset()

# check if API secret key was informed and ask for it input if not
try:
    assert (api_key != ""), "API key was not informed!"
except AssertionError as e:
    api_key = input("Input the API key: ")

# request forecast data from the API
url = "https://api.openweathermap.org/data/2.5/forecast?q=%s,%s&mode=json&appid=%s" % (city, country, api_key)
r = requests.get(url, timeout=3)

# check if request was successful and raise exception if not
assert (r.status_code == 200), "Request failed! Status code: " + str(r.status_code)

# initialize list
data = []
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for i in week_days:
    data.append([0, 0, i])

# parse JSON data into list
raw = r.json()

for i in raw["list"]:
    dia = time.localtime(i["dt"]).tm_wday
    data[dia][0] += 1
    data[dia][1] += i["main"]["humidity"]

# rearrange list so today is first
index = time.localtime(time.time()).tm_wday
data = data[index:] + data[:index]

# find out the days with high probability of raining
# it will also give forecast for today if run before 09:00 AM
rainy_days = []

for i, j in enumerate(data):
    if j[0] > 3:  # ignore days with less than 3 data points
        if j[1]/j[0] > 70:
            rainy_days.append(j[2])

# format and print the forecast
forecast = "You should take an umbrella in these days:\033[1m\u001b[34m"  # colorize output with ANSI escape codes
n = len(rainy_days)

for i in range(n-2):
    forecast += " " + rainy_days[i] + ","
forecast += " " + rainy_days[n - 1] + "."

print(forecast)
