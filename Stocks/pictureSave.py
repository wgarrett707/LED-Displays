#!/usr/bin/env python
import time
#from rgbmatrix import RGBMatrix, RGBMatrixOptions
#from samplebase import SampleBase
from PIL import Image, ImageDraw, ImageFont

#options = RGBMatrixOptions()
#options.rows = 32
#options.chain_length = 1
#options.parallel = 1
#options.hardware_mapping = 'regular'
#options.brightness = 30
#options.multiplexing = 6
#options.led_rgb_sequence = "BGR"
#options.pwm_lsb_nanoseconds = 350

#matrix = RGBMatrix(options = options)

stockSymbols = ["AAL", "AAPL", "ABT", "ADBE", "AMD", "AMZN", "AXP", "BA",
                "BBBY", "BBY", "BIG", "BP", "BRK-A", "CAT", "CBS", "COF",
                "COST", "CSCO", "CVS", "CVX", "DELL", "DG", "DIS", "DLTR",
                "DNKN", "DOW", "EBAY", "F", "FB", "FDX", "FITB", "GE", "GIS",
                "GM", "GOOG", "GS", "HAS", "HD", "HPQ", "HSBC", "HSY", "IBM",
                "KO", "MCD", "MMM", "NSRGY", "SVNDY", "XON"]

index = 0

while True:
    if index <= len(stockSymbols) - 1:
        readingFile = open("stocks.txt", "r")
        lines = readingFile.readlines()
        
        values = lines[index].split()
        print(values[1])
        
        img = Image.new('RGBA', (150, 25), color = (0, 0, 0, 0))
 
        arialFont = ImageFont.truetype('arial.ttf', size=19)
        d = ImageDraw.Draw(img)
        d.text((0, 0), values[1], font=arialFont, fill=(255, 255, 255))
        textWidth, textHeight = d.textsize(values[1], font=arialFont)
        img = img.crop((0, 4, textWidth, textHeight))
        fileName = values[0] + ".png"
        img.save(fileName)
        
        index += 1
    else:
        index = 0

