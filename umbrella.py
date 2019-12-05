"""
@title:: Umbrella 1.0
@description: Get weather forecast data from openweathermap.com and tells for the week which days you should take an
umbrella when you leave home.
@author: Daniel de Souza Telles
@email: danieldesouzatelles@gmail.com
"""

import requests
import time

# script configuration
api_key = ""
city = "Ribeirão Preto"
country = "BR"

# check if API secret key was informed and ask for it input if not
try:
    assert (api_key != ""), "API key was not informed!"
except AssertionError as e:
    api_key = input("Input the API key: ")

#  request forecast data from the API
url = "https://api.openweathermap.org/data/2.5/forecast?q=%s,%s&mode=json&appid=%s" % (city, country, api_key)
r = requests.get(url, timeout=3)

# check if request was successful and raise exception if not
assert (r.status_code == 200), "Request failed! Status code: " + str(r.status_code)

# parse JSON data into a list
raw = r.json()
data = [[0, 0] for i in range(7)]

for i in raw["list"]:
    dia = time.gmtime(i["dt"]).tm_wday
    data[dia][0] += 1
    data[dia][1] += i["main"]["humidity"]

# find out the days with high probability of raining
week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
rainy_days = []

for i, j in enumerate(data):
    if j[0] > 5:  # ignore days with less than 5 data points
        if j[1]/j[0] > 70:
            rainy_days.append(week_days[i])

# format and print the forecast
forecast = "You should take an umbrella in these days:"
n = len(rainy_days)

for i in range(n-2):
    forecast += " " + rainy_days[i] + ","
forecast += " " + rainy_days[n - 1] + "."

print(forecast)