import requests
import time

WAIT_TIME = 15 # seconds

class Nasfaq:
    def __init__(self) -> None:
        self.session, self.headers, self.cookies = self.getSession()
        self.session.headers.update(self.headers)
        #self.session.cookies.update(self.cookies)

    def getSession(self):
        session = requests.Session()
        multi_line = []
        line = input()
        while line:
            multi_line.append(line)
            line = input()

        multi_line.pop(0) # first line is the get 
        multi_line.pop(-1) # last line is just enter

        headers = {}
        for l in range(len(multi_line)):
            multi_line[l] = multi_line[l].split(':')
            multi_line[l][1] = multi_line[l][1][1:] # first character is always whitespace
            headers.update({multi_line[l][0] : multi_line[l][1]})

        return session, headers, headers['Cookie']

    def getURL(self, url):
        success = False
        while not success:
            try:
                resp = requests.get(url, headers=self.headers)

                if resp.status_code == requests.codes.ok:
                    return resp
            except Exception as e:
                print('failed... ', e)
                time.sleep(WAIT_TIME)
                print('retrying')

if __name__ == '__main__':
    nasfaq = Nasfaq()
    r = nasfaq.getURL("https://nasfaq.biz/api/getGachaboard")
    gachaBoard = r.json()['gachaboard']
