#!/usr/bin/env python3.7
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import time

fontBig = ImageFont.truetype('6x11.ttf', size=32)
fontMedium = ImageFont.truetype('6x11.ttf', size=16)
fontSmall = ImageFont.truetype('5x5.ttf', size=10)

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
    request = requests.get('') # api link
    weatherJson = request.json()
    print(weatherJson['main']['temp'])
    temperature = str(round(((weatherJson['main']['temp'] - 273.15) * 9/5) + 32))
    feelslike = str(round(((weatherJson['main']['feels_like'] - 273.15) * 9/5) + 32))
    #humidity = str(weatherJson['main']['humidity'])
    #windSpeed = str(round(weatherJson['wind']['speed'] * 2.23694))
    weatherIcon = Image.open('./icons/' + findIcon(weatherJson['weather'][0]['icon']))
    weatherX, forecastX = getXCoord(len(temperature), len(feelslike))
    print(temperature, feelslike)

    img = Image.new('RGBA', (256, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.fontmode = '1'
    dateNow = datetime.now()
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
    d.text((forecastX, 21), 'TEST LOL', font=fontSmall)

    img.save('test.png')

    waitAMinute(dateNow.minute)

main()
