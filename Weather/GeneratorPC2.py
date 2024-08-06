#!/usr/bin/env python3.7
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import time

fontBig = ImageFont.truetype('6x11.ttf', size=32)
fontMedium = ImageFont.truetype('6x11.ttf', size=16)
fontSmall = ImageFont.truetype('5x5.ttf', size=10)

# Maybe resort this into a dictionary?
def findIcon(code):
    if code.startswith('01'):
        return '1.png'
    elif code.startswith('02'):
        return '2.png'
    elif code.startswith('03') or code.startswith('04'):
        return '3.png'
    elif code.startswith('09'):
        return '4.png'
    elif code.startswith('10'):
        return '5.png'
    elif code.startsiwth('11'):
        return '6.png'
    elif code.startswith('13'):
        return '7.png'
    elif code.startswith('50'):
        return '8.png'

def getFahrenheit(num):
   return str(round(((num - 273.15) * 9/5) + 32)) 

# The x position of the little "°F" sign changes depending on how many numbers
# are in the temperature. This function helps with that.
def getXCoord(t, fl):
    if t == 1:
        #153
        return 127, fl * 5 + 144 - (3 - fl)
    if t == 2:
        if fl == 3:
            return 141, 159
        else:
            return 141, 155
    if t == 3:
        return 155, 169

def waitAMinute(minutes):
    while True:
        if datetime.now().minute != minutes:
            print('Minute has passed.')
            main()
            return
        else:
            time.sleep(1)

def main():
    global matrixCanvas
    dateNow = datetime.now()
    request = requests.get('') # api link
    weatherJson = request.json()
    request = requests.get('') # api link for forecast
    forecastJson = request.json()

    fcIterator = 0
    gotHigh = False
    passedToday = False
    fmtNow = dateNow.strftime('%Y-%m-%d')
    getHigh = True
    fcDays = []
    fcTemps = []

    # Maybe this will fix the error I keep getting whenever I first launch this script...
    try: forecastJson['properties']['periods']
    except: print('Errored out on the JSON')

    # Collects a dictionary that contains the next 5 days worth of highs and lows
    for daily in forecastJson['properties']['periods']:
        if fcIterator == 5:
            break
        if not passedToday:
            if fmtNow in daily['startTime']:
                continue
            else:
                passedToday = True

        # Because of how the API is organized, each day's high and low are in
        # two separate sections. This code checks to see if the iterator is
        # even, which means the section has the high, or odd, which means the
        # section has the low.
        if getHigh:
            dayName = daily['name'][:3]
            fcDays.append(dayName)
            fcTemps.append(str(daily['temperature']))
            getHigh = False
        else:
            fcTemps[fcIterator] += " " + str(daily['temperature'])
            getHigh = True
            fcIterator += 1

    print(fcDays, fcTemps)  
    print(weatherJson['main']['temp'])
    temperature = getFahrenheit(weatherJson['main']['temp'])
    feelslike = getFahrenheit(weatherJson['main']['feels_like'])
    #humidity = str(weatherJson['main']['humidity'])
    #windSpeed = str(round(weatherJson['wind']['speed'] * 2.23694))
    weatherIcon = Image.open('./icons/' + findIcon(weatherJson['weather'][0]['icon']))
    weatherX, forecastX = getXCoord(len(temperature), len(feelslike))
    print(temperature, feelslike)

    img = Image.new('RGBA', (256, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.fontmode = '1'
    currentTime = dateNow.strftime('%I:%M')
    AMPMstatus = dateNow.strftime('%p')
    currentDate = dateNow.strftime('%a %b %d')

    # Time and Date
    d.text((1, 1), currentTime, font=fontBig)
    if AMPMstatus == 'AM':
        d.text((63, 1), AMPMstatus, font=fontMedium, fill=(255, 102, 102))
    else:
        d.text((63, 12), AMPMstatus, font=fontMedium, fill=(153, 102, 255))
    
    d.text((1, 21), currentDate, font=fontSmall)

    # Weather
    img.paste(weatherIcon, (80, 0))
    d.text((113, 1), temperature, font=fontBig)
    d.text((weatherX, 1), '°F', font=fontMedium)
    d.text((113, 21), 'FL: ' + feelslike + '°F', font=fontSmall)

    # Forecast
    for i in range(0, 5):
        d.text((forecastX, i * 5 - 3 + i), fcDays[i] + "  " + fcTemps[i], font=fontSmall)

    img.save('test.png')

    waitAMinute(dateNow.minute)

main()
