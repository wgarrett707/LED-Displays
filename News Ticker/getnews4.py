from PIL import Image, ImageDraw, ImageFont
from newsapi import NewsApiClient
import time
import math

# Declare constants
NEWS_API = NewsApiClient(api_key='') # api key goes here
TEXT_FONT = ImageFont.truetype('arial.ttf', size=26)
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

# NOTE: THIS LOOP JUST GENERATES THE PHOTOS TO BE SHOWN. IT DOESN'T DO ANY OF THE DISPLAYING.
while done == False:
    # Create a new image and the ability to draw on it
    img = Image.new('RGBA', (STANDARD_WIDTH, 32), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # On the first iteration, grab the first title and get its dimensions
    if i == 0:
        title = titleList[titleNum]
        firstWidth, firstHeight = d.textsize(title, font=TEXT_FONT)
    # Get the dimensions of the current title being displayed
    hlWidth, hlHeight = d.textsize(title, font=TEXT_FONT)
    # This if-statement makes sure that the current title being shown still has room to be shown even after scrolling a set amount of pixels (ex. 500).
    # If it doesn't, then it won't be shown at all since the next title will be displayed.
    if xpos - STANDARD_WIDTH > -hlWidth:
        xpos -= STANDARD_WIDTH
        d.text((xpos, 1), title, font=TEXT_FONT, fill=(255, 255, 255))
    # This if-statement is just to make sure that the very first article title has already been shown and there is room for the next one.
    if i >= math.floor(firstWidth/500):
        # This only runs if the next article title is waiting to be shown. This happens when another article title is already fully on-screen and there is no room for the next one.
        if waiting:
            # This continues waiting if the first article STILL is fully on-screen even after another complete scroll.
            if start >= STANDARD_WIDTH:
                start -= STANDARD_WIDTH
                waiting = True
            # If it's now able to be on-screen and thus done waiting, the next article is pasted along with the separator (the little circle).
            else:
                d.text((start, 1), startTitle, font=TEXT_FONT, fill=(255, 255, 255))
                img.paste(SEPARATOR, (start - 32, 0))
                waiting = False
                # This makes the article that was waiting to be shown the MAIN article the script will focus on. 
                title = startTitle
                xpos = start

        #If there is no article waiting to be shown, then the script identifies the next article to be shown. This article may then wait, meaning this process is a continuous cycle.
        else:
            startNum += 1
            # This checks to make sure the script isn't past the range of generated articles. If it is, it marks that it's done and the 'while' loop ends.
            if startNum == len(titleList):
                done = True
            else:
                startTitle = titleList[startNum]
            # A quick formula to figure out where the next article currently is.
            start = hlWidth - STANDARD_WIDTH + start + 32
            # If it's starting position is currently off-screen, then it waits until the next iteration (after scrolling a set amount of pixels, like 500).
            if start >= 500:
                start -= 500
                waiting = True
            # If it's currently going to be on screen, then it places it on the screen with the separator and becomes the MAIN article the script will focus on.
            else:
                d.text((start, 1), startTitle, font=TEXT_FONT, fill=(255, 255, 255))
                img.paste(SEPARATOR, (start - 32, 0))
                title = startTitle
                xpos = start

    # This saves the image and prints out some information about it.
    img.save('./displays/' + str(i) + '.png')
    print('Completed.')
    print('hlWidth: ' + str(hlWidth) + '\nxpos: ' + str(xpos) + '\nstartNum: ' + str(startNum))
    i += 1


