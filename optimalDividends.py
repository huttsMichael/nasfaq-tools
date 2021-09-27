import requests
import json
import time
from datetime import datetime

WAIT_TIME = 15 # seconds
ADJUSTMENT_INTERVAL = ((24 * 6 * 60) + (20 * 60)) * 60 # (mins in first 6 days of week + mins in last day) * secs

class Dividends():
    def __init__(self, file = "dividends.json") -> None:
        self.filename = file
        self.histDividends = self.load()
        self.updateDividends = self.__renew()
        self.currentDividends, self.currentPrices = self.get()
        self.currentMembers = self.members()
        self.histDates = self.dates()
        
    def __renew(self):
        for ts in self.histDividends:
            timestamp = int(ts)
            if timestamp > 10000000000: 
                timestamp /= 1000 # timestamps had milliseconds added, divide those out if needed
            lastTime = datetime.utcfromtimestamp(timestamp)
        
        diffTime = datetime.now() - lastTime
        diffTimeSeconds = (diffTime.days * 86400) + diffTime.seconds # days * seconds in day + extra seconds
        print(ADJUSTMENT_INTERVAL, diffTimeSeconds, diffTime.days, diffTime.seconds)

        if diffTimeSeconds < ADJUSTMENT_INTERVAL: # no need to call getDividends if it's been too early
            return False
        else:
            return True

    def __getTrends(self):
        print(self.currentMembers)
    
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
        rawPrices = getURL("https://nasfaq.biz/api/getMarketInfo?all&history")
        prices = rawPrices.json()['coinInfo']['data']

        return dividends, prices

    def members(self):
        # initialize dict with all members
        allMembers = {}
        for holo in self.currentPrices:
            allMembers[holo] = []
        for div in self.histDividends:
            for holo in self.histDividends[div]:
                try:
                    allMembers[holo].append(self.histDividends[div][holo])
                except KeyError:
                    pass
        return allMembers

    def dates(self):
        allDates = []
        for date in self.histDividends:
            date = int(date)
            if date > 10000000000: 
                date /= 1000
            allDates.append(datetime.fromtimestamp(int(date)))

        return allDates

    def trends(self):
        self.__getTrends()

def getURL(url, session=""):
    success = False
    while not success:
        try:
            if session:
                resp = requests.get(url, cookies=session)
            else:
                resp = requests.get(url)
            if resp.status_code == requests.codes.ok:
                return resp
        except Exception as e:
            print('failed... ', e)
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
    #divs.trends()
    
    