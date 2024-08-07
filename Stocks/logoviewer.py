#!/usr/bin/env python

import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
from PIL import Image

stockSymbols = ["AAL", "AAPL", "ABT", "ADBE", "AMD", "AMZN", "AXP", "BA",
                "BBBY", "BBY", "BIG", "BP", "BRK-A", "CAT", "CBS", "COF",
                "COST", "CSCO", "CVS", "CVX", "DELL", "DG", "DIS", "DLTR",
                "DNKN", "DOW", "EBAY", "F", "FB", "FDX", "FITB", "GE", "GIS",
                "GM", "GOOG", "GS", "HAS", "HD", "HPQ", "HSBC", "HSY", "IBM",
                "KO", "MCD", "MMM", "NSRGY", "SVNDY", "XON"]

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.multiplexing = 6
options.brightness = 30
options.led_rgb_sequence = "BGR"
options.pwm_lsb_nanoseconds = 350

matrix = RGBMatrix(options = options)
print("Press CTRL-C to stop.")
index = 0

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        print("test1.1")
        super(ImageScroller, self).__init__(*args, **kwargs)
        print("test1.2")
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")
        print("test1.3")

    def run(self):
        image_file = stockSymbols[index] + ".png"
        image = Image.open(image_file)

        # Make image fit our screen.
        # image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

        matrix.SetImage(image.convert('RGB'))
        
        double_buffer = self.matrix.CreateFrameCanvas()
        index = index + 1
        
        xpos = 0

        while True:
            if (xpos <= img_width):
                xpos += 1
                double_buffer.SetImage(image, -xpos)
                double_buffer.SetImage(image, -xpos + img_width)

                double_buffer = self.matrix.SwapOnVSync(double_buffer)
                time.sleep(0.5)
            else:
                break
        
        if index > len(stockSymbols):
            index = 0

        print("test")
        
    print("test88")
        
        

if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
