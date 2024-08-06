from PIL import Image, ImageDraw, ImageFont
from newsapi import NewsApiClient
import time
import math

# Declare constants
NEWS_API = NewsApiClient(api_key='') # api key goes here
textFont = ImageFont.truetype('arial.ttf', size=26)
STANDARD_WIDTH = 500
SEPARATOR = Image.open('separator.png')

# Get the top headlines 
top_headlines = NEWS_API.get_top_headlines(category='business',
                                          language='en',
                                          country='us',
                                          page_size=100)['articles']

# Declare variables for 'while' loop
xpos = 500
start = 0
i = 0
titleNum = 0
startNum = 0
done = False
waiting = False

# Create list of article titles
titleList = []
for article in top_headlines:
    titleList.append(article['title'])

while done == False:
    img = Image.new('RGBA', (STANDARD_WIDTH, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    #d.fontmode = '1'
    if i == 0:
        title = titleList[titleNum]
        firstWidth, firstHeight = d.textsize(title, font=textFont)
    hlWidth, hlHeight = d.textsize(title, font=textFont)
    if xpos - STANDARD_WIDTH > -hlWidth:
        xpos -= STANDARD_WIDTH
        d.text((xpos, 1), title, font=textFont, fill=(255, 255, 255))
    if i >= math.floor(firstWidth/500):
        if waiting:
            if start >= STANDARD_WIDTH:
                start -= STANDARD_WIDTH
                waiting = True
            else:
                d.text((start, 1), startTitle, font=textFont, fill=(255, 255, 255))
                img.paste(SEPARATOR, (start - 32, 0))
                waiting = False
                title = startTitle
                xpos = start
        else:
            startNum += 1
            try:
                startTitle = titleList[startNum]                  
            except:
                done = True
            start = hlWidth - STANDARD_WIDTH + start + 32
            if start >= 500:
                start -= 500
                waiting = True
            else:
                d.text((start, 1), startTitle, font=textFont, fill=(255, 255, 255))
                img.paste(SEPARATOR, (start - 32, 0))
                title = startTitle
                xpos = start

    img.save('./displays/' + str(i) + '.png')
    print('Completed.')
    print('hlWidth: ' + str(hlWidth) + '\nxpos: ' + str(xpos) + '\nstartNum: ' + str(startNum))
    i += 1


