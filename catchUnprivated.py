import time
from optimalDividends import getURL

CHECK_INTERVAL = 60

class Channels:
    def __init__(self) -> None:
        self.data = self.get()
        self.diffs, self.streams = self.analyze()
        self.uploads = self.count()

    def get(self):
        # get data of all channels' status 
        statusA = getURL("https://api.holotools.app/v1/channels?offset=0&limit=50")
        statusB = getURL("https://api.holotools.app/v1/channels?offset=50&limit=50")
        status = statusA.json()['channels']

        for channel in statusB.json()['channels']:
            status.append(channel)

        # get data of upcoming streams
        streams = getURL("https://jetrico.sfo2.digitaloceanspaces.com/hololive/youtube.json")
        
        return(status, streams)

    def count(self):
        # currently redudant check, keep track of total uploaded videos so new videos don't count as unprivated videos
        videos = []

        for channel in self.data:
            videos.append(channel['video_original'])

        return videos

    def analyze(self):
        diffs = []

        for channel in self.data:
            diffs.append(channel['video_original'] - channel['video_count'])

        return(self.correct(diffs))
    
    def check(self):
        self.data = self.get()
        diffs = self.analyze()
        uploads = self.count()

        videoFound = False
        for n in range(len(diffs)):
                if diffs[n] != self.diffs[n] and uploads[n] == self.uploads[n]:
                    videoFound = True
                    print("Change found with: {}  ---  ({} vs {}, {} vs {})"
                        .format(self.data[n]['name'], diffs[n], self.diffs[n], uploads[n], self.uploads[n]))
                    if diffs[n] < self.diffs[n]:
                        print("Change type: UNPRIVATED VIDEO")
                    elif diffs[n] > self.diffs[n]:
                        print("Change type: PRIVATED VIDEO")

        self.diffs = diffs
        self.uploads = uploads
        return(videoFound)
    
if __name__ == '__main__':
    print("Initializing...", end=' ')
    ch = Channels()
    print("Done!")
    while True:
        time.sleep(CHECK_INTERVAL)
        if ch.check():
            print("CHANGES FOUND")
        else:
            print("no changes found")
    
