import requests
import json
from optimalDividends import getURL

class Gachaboard:
    def __init__(self) -> None:
        self.session = {"holosesh": "s%3ATrOhWfPnHw4QhjjgDCGnHJut8xFZEf-V.3QNRdhQGzh6vak7VAJ3oehj5QGAYlDPEZW%2F363CvH%2F4"}
        self.data = getURL("https://nasfaq.biz/api/getGachaboard", session=self.session)
    
    def display(self):
        print(self.data.json())



if __name__ == '__main__':
    print("Initializing...", end=' ')
    ch = Gachaboard()
    print("Done!")
    ch.display()