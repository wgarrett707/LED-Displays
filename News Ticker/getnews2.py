from PIL import Image, ImageDraw, ImageFont
from newsapi import NewsApiClient
import time
import math

newsapi = NewsApiClient(api_key='') # api key goes here
textFont = ImageFont.truetype('arial.ttf', size=26)
headlineList = []
STANDARD_WIDTH = 500

top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us')['articles']

xpos = 500
start = 0
i = 0
titleNum = 0
startNum = 0
done = False
waiting = False
while done == False:
    img = Image.new('RGBA', (STANDARD_WIDTH, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    #d.fontmode = "1"
    if i == 0:
        title = top_headlines[titleNum]['title']
        firstWidth, firstHeight = d.textsize(title, font=textFont)
    hlWidth, hlHeight = d.textsize(title, font=textFont)
    if xpos - 500 > -hlWidth:
        xpos -= 500
        d.text((xpos, 1), title, font=textFont, fill=(255, 255, 255))
    if i >= math.floor(firstWidth/500):
        if waiting:
            if start >= 500:
                start -= 500
                waiting = True
            else:
                d.text((start, 1), startTitle, font=textFont, fill=(255, 255, 255))
                waiting = False
                title = startTitle
                xpos = start
        else:
            startNum += 1
            startTitle = top_headlines[startNum]['title']
            start = hlWidth - STANDARD_WIDTH + start
            if start >= 500:
                start -= 500
                waiting = True
            else:
                d.text((start, 1), startTitle, font=textFont, fill=(255, 255, 255))
                title = startTitle
                xpos = start

    img.save('test' + str(i) + '.png')
    print('Completed.')
    print('hlWidth: ' + str(hlWidth) + '\nxpos: ' + str(xpos))
    time.sleep(2)
    i += 1
    if i == 8:
        time.sleep(99999999999999)


