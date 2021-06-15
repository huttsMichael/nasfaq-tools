import time
from optimalDividends import getURL

CHECK_INTERVAL = 900

class Channels:
    def __init__(self) -> None:
        self.data, self.streams = self.get()
        self.diffs = self.analyze()
        self.status = self.live()
        self.uploads = self.count()

    def get(self):
        # get data of all channels' status 
        dataA = getURL("https://api.holotools.app/v1/channels?offset=0&limit=50")
        dataB = getURL("https://api.holotools.app/v1/channels?offset=50&limit=50")
        data = dataA.json()['channels']

        for channel in dataB.json()['channels']:
            data.append(channel)

        # get data of upcoming streams
        streams = getURL("https://jetrico.sfo2.digitaloceanspaces.com/hololive/youtube.json").json()
        
        return(data, streams)

    def live(self):
        status = [False] * len(self.diffs)
        ongoing = self.streams['live']
        for channelIndex in range(len(self.data)):
            for stream in ongoing:
                if self.data[channelIndex]['id'] == stream['channel']['id']:
                    status[channelIndex] = True
        return status

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

        return(diffs)
    
    def check(self):
        self.data, self.streams = self.get()
        diffs = self.analyze()
        uploads = self.count()

        videoFound = False
        for n in range(len(diffs)):
                if diffs[n] != self.diffs[n] and uploads[n] == self.uploads[n] and self.status[n] == False:
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
    
