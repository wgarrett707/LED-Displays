import yfinance as yf
import os

stockSymbols = ["AAL", "AAPL", "ABT", "ADBE", "AMD", "AMZN", "AXP", "BA",
                "BBBY", "BBY", "BIG", "BP", "BRK-A", "CAT", "CBS", "COF",
                "COST", "CSCO", "CVS", "CVX", "DELL", "DG", "DIS", "DLTR",
                "DNKN", "DOW", "EBAY", "F", "FB", "FDX", "FITB", "GE", "GIS",
                "GM", "GOOG", "GS", "HAS", "HD", "HPQ", "HSBC", "HSY", "IBM",
                "KO", "MCD", "MMM", "NSRGY", "SVNDY", "XON"]

global index
index = 1

if os.path.exists("stocks.txt"):
    print("Good to go! stocks.txt already exists!")
else:
    testingFile = open("stocks.txt", "x")
    testingFile.close()
    
testingFile = open("stocks.txt", "r")
lines = testingFile.readlines()
testingFile.close()

if lines == []:
    testingFile = open("stocks.txt", "w")
    while index <= len(stockSymbols):
        testingFile.write("placeholder \n")
        index += 1

testingFile.close()

while True:
    readingFile = open("stocks.txt", "r")
    lines = readingFile.readlines()
    index = 0

    while index <= len(stockSymbols) - 1:
        selectedSymbol = stockSymbols[index]
        yfSymbol = yf.Ticker(selectedSymbol)
        whatToWrite = str(selectedSymbol) + " " + str(format(round(yfSymbol.info['regularMarketPrice'], 2), ".2f")) + " " + str(format(round(yfSymbol.info['regularMarketChange'], 2), ".2f")) + "\n"
        lines[index] = whatToWrite
        writingFile = open("stocks.txt", 'w')
        writingFile.writelines(lines)
        writingFile.close()
        index += 1
        print(selectedSymbol + " done")
