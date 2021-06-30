import requests
import json
import time
from datetime import datetime

WAIT_TIME = 15 # seconds

class Dividends():
    def __init__(self, file = "dividends.json") -> None:
        self.filename = file
        self.histDividends = self.load()
        self.updateDividends = self.__renew()
        self.currentDividends, self.currentPrices = self.get()
        
    def __renew(self):
        for ts in self.histDividends:
            timestamp = int(ts)
            if timestamp > 10000000000: 
                timestamp /= 1000 # timestamps had milliseconds added, divide those out if needed
            lastTime = datetime.utcfromtimestamp(timestamp)
        
        diffTime = datetime.now() - lastTime

        if diffTime.days < 6: # no need to call getDividends if 
            return False
        else:
            return True
    
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
            
    def get(self):
        print("Get dividends")
        
        if self.updateDividends:
            print("There should be new dividends!")
            rawDividends = getURL("https://nasfaq.biz/api/getDividends")
            dividends = rawDividends.json()['dividends']['payouts']
            self.log(rawDividends)
        else:
            # use old dividend data if it hasn't been updated
            for ts in self.histDividends:
                dividends = self.histDividends[ts]

        print("Get prices")
        rawPrices = getURL("https://nasfaq.biz/api/getMarketInfo")
        prices = rawPrices.json()['coinInfo']['data']

        return dividends, prices

def getURL(url):
    success = False
    while not success:
        try:
            resp = requests.get(url)
            if resp.status_code == requests.codes.ok:
                return resp
        except:
            print('failed... ', end='')
            time.sleep(WAIT_TIME)
            print('retrying')


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
    divs = Dividends()
    calc = calculateRatios(divs.currentDividends, divs.currentPrices)
    ratios = sortRatios(calc, descending=True)
    for holo in ratios:
        print(holo + ": " + "%.3f" % ratios[holo])
    
    