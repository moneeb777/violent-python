import urllib
from webRecon import anonBrowser, mirrorImages, printLinks
import json

class googleResult():
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

    def __repr__(self):
        return self.title


def google(searchTerm):
    ab = anonBrowser()
    searchTerm = urllib.quote_plus(searchTerm)
    response = ab.open('http://ajax.googleapis.com/' + 'ajax/services/search/web?v=1.0&q=' + searchTerm)
    objects = json.load(response)
    results = []
    for result in objects['responseData']['results']:
        url = result['url'].encode('utf8')
        title = result['content'].encode('utf8')
        text = result['content'].encode('utf8')
        newGr = googleResult(title, text, url)
        results.append(newGr)
    return results

def main():
    keyword = 'Boondock Saint'
    results = google(keyword)
    print results

if __name__ == '__main__':
    main()