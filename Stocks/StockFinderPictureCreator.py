#!/usr/bin/env python
import time
#from rgbmatrix import RGBMatrix, RGBMatrixOptions
#from samplebase import SampleBase
from PIL import Image, ImageDraw, ImageFont
import yfinance as yf

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
        selectedSymbol = stockSymbols[index]
        yfSymbol = yf.Ticker(selectedSymbol)
        symbolPrice = format(round(yfSymbol.info['regularMarketPrice'], 2), ".2f")
        symbolChange = format(round(yfSymbol.info['regularMarketChange'], 2), ".2f")
        print(selectedSymbol, symbolPrice, symbolChange)
        if symbolChange.find("-") == -1:
            textRed = 0
            textGreen = 255
            arrowFile = "uparrow.png"
        else:
            textRed = 255
            textGreen = 0
            arrowFile = "downarrow.png"
        
        img = Image.new('RGBA', (400, 18), color = (0, 0, 0, 0))
        textFont = ImageFont.truetype('calibrib.ttf', size=22)
        d = ImageDraw.Draw(img)
        d.text((0, 0), symbolPrice, font=textFont, fill=(textRed, textGreen, 0))
        arrowImage = Image.open(arrowFile)
        priceWidth, priceHeight = d.textsize(symbolPrice, font=textFont)
        img.paste(arrowImage, (priceWidth + 4, 3))
        d.text((priceWidth + 15, 0), symbolChange, font=textFont, fill=(textRed, textGreen, 0))
        changeWidth, changeHeight = d.textsize(symbolChange, font=textFont)
        img.save("test.png")
        img = img.crop((0, 3, priceWidth + 15 + changeWidth, priceHeight))
        fileName = selectedSymbol + ".png"
        img.save(fileName)
        quit()
        index += 1
    else:
        index = 0
