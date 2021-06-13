import requests
import json
import time

class Dividends():
    def __init__(self, file = "dividends.json") -> None:
        self.filename = file
        self.histDividends = self.load()
        self.currentDividends, self.currentPrices = self.get() # getDivs should check if divs are old
        
    def load(self):
        with open("dividends.json") as divs:
            hist = json.load(divs)
        return hist

    def log(self, rawDividends):
        print("\nLogging dividends")
        newDate = True
        for timestamp in self.histDividends:
            if str(rawDividends.json()['dividends']['timestamp']) == timestamp:
                newDate = False
            else:
                print(str(rawDividends.json()['dividends']['timestamp']), "and", timestamp, "are not equal")

        if newDate:
            print("new date!", timestamp, "\n")
            self.histDividends[str(rawDividends.json()['dividends']['timestamp'])] = rawDividends.json()['dividends']['payouts']
            with open("dividends.json", 'w') as divs:
                json.dump(self.histDividends, divs)
        else:
            print("no new data\n")
            
    def get(self, average = False):
        print("Get dividends")
        rawDividends = requests.get("https://nasfaq.biz/api/getDividends")
        if not average:
            dividends = rawDividends.json()['dividends']['payouts']
        else:
            dividends = {}
        self.log(rawDividends)

        print("Get prices")
        rawPrices = requests.get("https://nasfaq.biz/api/getMarketInfo")
        prices = rawPrices.json()['coinInfo']['data']

        return dividends, prices

def calculateRatios(dividends, prices):
    print("\nCalculating ratios")
    ratios = {}
    for holo in prices:
        try:
            ratios[holo] = dividends[holo]/prices[holo]['price']
        except:
            print(holo, "does not exist")

    return ratios

def sortRatios(unsortedRatios, descending=False):
    print("\nSorting ratios")
    return dict(sorted(unsortedRatios.items(), key=lambda item: item[1], reverse=descending))

if __name__ == '__main__':
    failed = True
    while failed:
        try:
            divs = Dividends()
            failed = False
        except:
            print("Failed... ", end='')
            time.sleep(15)
            print("Retrying")
            continue
    
    calc = calculateRatios(divs.currentDividends, divs.currentPrices)
    ratios = sortRatios(calc, descending=True)
    for holo in ratios:
        print(holo + ": " + "%.3f" % ratios[holo])
    
    