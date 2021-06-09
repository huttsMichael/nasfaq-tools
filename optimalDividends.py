import requests
import json
import time

def loadDividends():
    with open("dividends.json") as divs:
        histDividends = json.load(divs)
    return histDividends

def logDividends(rawDividends):
    print("\nLog dividends")
    histDividends = loadDividends()

    newDate = True
    for timestamp in histDividends:
        if str(rawDividends.json()['dividends']['timestamp']) == timestamp:
            newDate = False
        else:
            print(str(rawDividends.json()['dividends']['timestamp']), "and", timestamp, "are not equal")

    if newDate:
        print("new date!", timestamp, "\n")
        histDividends[str(rawDividends.json()['dividends']['timestamp'])] = rawDividends.json()['dividends']['payouts']
        with open("dividends.json", 'w') as divs:
            json.dump(histDividends, divs)
    else:
        print("no new data\n")
        
def getDividends(average = False):
    print("Get dividends")
    rawDividends = requests.get("https://nasfaq.biz/api/getDividends")
    if not average:
        dividends = rawDividends.json()['dividends']['payouts']
    else:
        dividends = {}
    logDividends(rawDividends)

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
            div, price = getDividends()
            failed = False
        except:
            time.sleep(5)
            continue

    failed = True
    while failed:
        try:
            calc = calculateRatios(div, price)
            ratios = sortRatios(calc, descending=True)
            for holo in ratios:
                print(holo + ": " + "%.3f" % ratios[holo])
            failed = False
        except:
            print("Failed... ", end='')
            time.sleep(10)
            print("Retrying")
            continue
    
    