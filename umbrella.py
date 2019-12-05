"""
@title:: Umbrella 1.0
@description: Get weather forecast data from openweathermap.com and tells for the week which days you should take an
umbrella when you leave home.
@author: Daniel de Souza Telles
@email: danieldesouzatelles@gmail.com
"""

import requests
import time

api_key = ""
cidade = "Ribeirão Preto"
pais = "BR"

assert (api_key != ""), "API Key is empty"

url = "https://api.openweathermap.org/data/2.5/forecast?q=%s,%s&mode=json&appid=%s" % (cidade, pais, api_key)

forecast = requests.get(url, timeout=3).json()

data = [[0, 0] for i in range(7)]

for i in forecast["list"]:
    dia = time.gmtime(i["dt"]).tm_wday
    data[dia][0] += 1
    data[dia][1] += i["main"]["humidity"]

semana = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
chuva = []

for i, j in enumerate(data):
    if j[0] > 1:
        if j[1]/j[0] > 70:
            chuva.append(semana[i])

n = len(chuva)
frase = "You should take an umbrella in these days:"

for i in range(n-2):
    frase += " " + chuva[i] + ","
frase += " " + chuva[n-1] + "."

print(frase)