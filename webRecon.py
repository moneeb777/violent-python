import mechanize
import cookielib
import random
import time
from BeautifulSoup import BeautifulSoup
import re
import os


class anonBrowser(mechanize.Browser):

    def __init__(self, proxies = [], user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201', \
                                                    'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:2.0b4) Gecko/20100818', \
                                                    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1b3) Gecko/20090305']):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)  # Disregard what robots.txt has to tell us
        self.proxies = proxies
        self.user_agents = user_agents + ['Mozilla/4.0 ', 'FireFox/6.01', 'ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        index = random.randrange(0, len(self.user_agents))
        self.addheaders = [('User-agent', (self.user_agents[index]))]

    def change_proxy(self):
        if self.proxies:
            index = random.randrange(0, len(self.proxies))
            self.set_proxies({'http': self.proxies[index]})

    def anonymize(self, sleep=False):  # Clear cookies, change user agent, change proxy
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        if sleep:
            time.sleep(60)


def printLinks(url):
    ab = anonBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    try:
        print '[+] Printing links from Regex'
        link_finder = re.compile('href="(.*?)"')
        links = link_finder.findall(html)
        for link in links:
            print link
    except:
        pass

    try:
        print '\n[+] Printing links from BeautifulSoup.'
        soup = BeautifulSoup(html)
        links = soup.findAll(name='a')
        for link in links:
            if link.has_key('href'):
                print link['href']
    except:
        pass

def mirrorImages(url, dir):
    ab = anonBrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html)
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src']
        print filename
        filename = str(filename.replace('/', '_')).lstrip('https://') + str('.jpg')
        filename = filename.replace('?', 'QUESTION')
        filename = os.path.join(dir, filename)
        print filename
        print '[+] Saving ' + str(filename)
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'w+')
        save.write(data)
        save.close()


def main():
    url = 'http://www.moneebazhar.wordpress.com'
    dir = os.getcwd()
    print dir
    if url == None or dir == None:
        exit(0)
    else:
        try:
            mirrorImages(url, dir)
        except Exception, e:
            print '[-] Error mirroring images'
            print '[-] ' + str(e)

if __name__ == '__main__':
    main()






