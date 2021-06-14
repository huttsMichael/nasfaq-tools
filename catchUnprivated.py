import time
from optimalDividends import getURL

CHECK_INTERVAL = 900

class Channels:
    def __init__(self) -> None:
        self.data = self.get()
        self.diffs = self.analyze()

    def get(self):
        dataA = getURL("https://api.holotools.app/v1/channels?offset=0&limit=50")
        dataB = getURL("https://api.holotools.app/v1/channels?offset=50&limit=50")
        dataC = dataA.json()['channels']

        for channel in dataB.json()['channels']:
            dataC.append(channel)
        
        return(dataC)
    
    def analyze(self):
        diffs = []

        for channel in self.data:
            diffs.append(channel['video_original'] - channel['video_count'])

        return(diffs)
    
    def check(self):
        self.data = self.get()
        diffs = self.analyze()

        videoFound = False
        for n in range(len(diffs)):
                if diffs[n] != self.diffs[n]:
                    videoFound = True
                    print("Change found with: ", self.data[n]['name'])
                    if diffs[n] < self.diffs[n]:
                        print("Change type: UNPRIVATED VIDEO")
                    elif diffs[n] > self.diffs[n]:
                        print("Change type: PRIVATED VIDEO")

        self.diffs = diffs
        return(videoFound)


    
if __name__ == '__main__':
    ch = Channels()
    
    while True:
        time.sleep(CHECK_INTERVAL)
        if ch.check():
            print("CHANGES FOUND")
        else:
            print("no changes found")
    
