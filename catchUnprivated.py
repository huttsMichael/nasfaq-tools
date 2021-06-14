import requests
import json
import time
from optimalDividends import getURL

class Channels:
    def __init__(self) -> None:
        self.data = self.get()

    def get(self):
        dataA = getURL("https://api.holotools.app/v1/channels?offset=0&limit=50")
        dataB = getURL("https://api.holotools.app/v1/channels?offset=50&limit=50")
        dataC = dataA.json()['channels']
        dataC.append(dataB.json()['channels'])
        return(dataC)

    
if __name__ == '__main__':
    ch = Channels()
    ch.get()
    for channel in ch.data:
        print(channel)
