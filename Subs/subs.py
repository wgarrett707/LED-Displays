from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
import json
import time
import math

api_key = '' # insert api key
channel_data = '' # insert channel ids
youtube = build('youtube', 'v3', developerKey=api_key)

font7 = ImageFont.truetype('5x7.ttf', size=16)
font5 = ImageFont.truetype('5x5.ttf', size=10)
iconTest = Image.open('./icons/1.png')
    
iconList = [Image.open('./icons/1.png'),
            Image.open('./icons/2.png'),
            Image.open('./icons/3.png')]

# TO-DO: Make a centering system that works. Right now it's a few squares off
# if you use big view counts
def findCenter(infoList):
    add = 0
    for i in range(0, len(infoList)):
        if int(infoList[i][1]) >= 99999:
            add += ((len(infoList[i][1]) - 5) * 6) - 2
    totalX = (len(iconList) * 64) + add
    print(totalX)
    return round(((256 - totalX)/2) - 2)
            
def listReturn(r):
    infoList = []
    for channel in r['items']:
        stats = channel['statistics']
        infoList.append((stats['subscriberCount'], stats['viewCount']))
    return infoList

def generateImage(infoList):
    img = Image.new('RGBA', (256, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.fontmode = '1'
    start = 0
    add = 0

    for i in range(0, len(infoList)):
        xpos = start + (i * 64) + add
        img.paste(iconList[i], (xpos, 0))
        d.text((xpos + 32, -3), 'SUBS:', font=font5)
        d.text((xpos + 32, 3), infoList[i][0], font=font7)
        d.text((xpos + 32, 13), 'VIEWS:', font=font5)
        d.text((xpos + 32, 19), infoList[i][1], font=font7)
        if int(infoList[i][1]) >= 99999:
            add += ((len(infoList[i][1]) - 5) * 6) - 2

    img.save('test.png')

def gatherData():
    request = youtube.channels().list(
        part='statistics',
        id=channel_data)

    response = request.execute()

    generateImage(listReturn(response))

gatherData()
