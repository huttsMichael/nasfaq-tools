import requests
import json
import time
import sys

MAX_RETRIES = 10
SLEEP_TIME = 30 # seconds
AUTO_BACKUP = False
DEBUG = True

def getLeaderboard():
    if DEBUG:
        print("sending request")
    rawLeaderboard = requests.get("https://nasfaq.biz/api/getLeaderboard?leaderboard&oshiboard", timeout=30)
    print("response received")

    timestamp = rawLeaderboard.json()['leaderboard']['timestamp']
    leaderboard = []

    for user in rawLeaderboard.json()['leaderboard']['leaderboard']:
        leaderboard.append(user)
    
    print("writing to file")
    with open('leaderboard.json', 'a') as outfile:
        #json.dump(rawLeaderboard.json()['timestamp'], outfile)
        outfile.write('"'+str(timestamp)+'":')
        json.dump(rawLeaderboard.json()['leaderboard']['leaderboard'], outfile)
        outfile.write(',')
    print("file written")
    
    return leaderboard

if __name__ == "__main__":
    try:
        with open('leaderboard.json', 'x') as outfile:
            outfile.write('{')
    except:
        with open('leaderboard.json', 'rb+') as f:
            f.seek(0,2)                 # end of file
            size=f.tell()               # the size...
            f.truncate(size-1)          # truncate at that size - how ever many characters
        with open('leaderboard.json', 'a') as outfile:
            outfile.write(',')
    retries = MAX_RETRIES
    while retries > 0:
        try:
            print(time.strftime("%H:%M:%S", time.localtime()), "retrieving leaderboard")
            getLeaderboard()
            print(time.strftime("%H:%M:%S", time.localtime()), "retrieved leaderboard")
            time.sleep(900)
            retries = MAX_RETRIES # reset retry counter if it runs succesfully
        except KeyboardInterrupt:
            print("\nfixing")
            with open('leaderboard.json', 'rb+') as f:
                f.seek(0,2)                 # end of file
                size=f.tell()               # the size...
                f.truncate(size-1)          # truncate at that size - how ever many characters
            with open('leaderboard.json', 'a') as outfile:
                outfile.write('}')
            print("fixed")
            retries = 0
        except requests.exceptions.ConnectionError:
            print("Request Failed:", sys.exc_info()[0])
            time.sleep(SLEEP_TIME + (retries * 5))
            continue
        except:
            print("Other Failure:", sys.exc_info()[0])
            if AUTO_BACKUP:
                timestr = time.strftime("%Y%m%d-%H%M%S")
                with open("leaderboard.json", "r") as source, open(timestr + "_leaderboard.json", "w") as dest:
                    dest.write(source.read())
            time.sleep(SLEEP_TIME + (retries * 5))
            retries -= 1
            print("Retries Remaining:", retries)
            continue

        