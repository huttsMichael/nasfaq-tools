import requests
import json
from optimalDividends import getURL

class Gachaboard:
    def __init__(self) -> None:
        self.session = {"holosesh": "TOKEN HERE"} # you have to get this manually. 
        self.data = getURL("https://nasfaq.biz/api/getGachaboard", session=self.session)
    
    def display(self):
        print(self.data.json())



if __name__ == '__main__':
    print("Initializing...", end=' ')
    ch = Gachaboard()
    print("Done!")
    ch.display()