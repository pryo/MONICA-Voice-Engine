
from bs4 import BeautifulSoup
import urllib.request as req
import re
import csv
import os

from numpy import unicode


def makeSoup(url):
    return BeautifulSoup(req.urlopen(url).read().decode('latin-1'))

def findLinkList(soup):
    return soup.find_all(linkFilter)
def linkFilter(tag):
    pattern = re.compile("Episode")
    if tag.get('href'):
        if tag.string and pattern.match(tag.string):
            if len(tag.find_parents("li")) != 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def pageFilter(tag):

    pattern = re.compile("Moinca|Rachel|Ross|Phoebe|Joey|Chandler")

    if tag.contents:
        try:
            if (tag.contents[0].name=='b' and pattern.match(tag.contents[0].string)):
                return True
        except(TypeError):
            return False

        else:
            return False
    else:
        return False

def pageFormatChecker(soup):
    # a lot of b tag inside p tag with roles name in it
    condition = (len(soup.find_all(pageFilter))>10)
    if condition:
        return True
    else:
        return False
def filePipeline(pageSoup,linkTag,relativePath):
    path = os.path.join(os.path.dirname(__file__),relativePath)
    #open a file according to the episode number and store the list of line in CSV format
    episodeNumberPattern =re.compile("\b[0-9]{3,4}")

    matchObj = episodeNumberPattern.match(unicode(linkTag.string))
    fileName = matchObj.string
    with open(path+fileName+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        lineList = pageSoup.find_all(pageFilter)
        for line in lineList:
            name = line.contents[0].string
            script = line.string
            writer.writerow([name, script])


if __name__ =="__main__":

    indexURL= 'http://www.livesinabox.com/friends/scripts.shtml'
    URLPrefix = 'http://www.livesinabox.com/friends/'
    relativePath = '../Data/Scripts/'
    indexSoup = makeSoup(indexURL)
    linkTagList = findLinkList(indexSoup)
    for linkTag in linkTagList:
        pageSoup = makeSoup(URLPrefix+linkTag.get('href'))
        if pageFormatChecker(pageSoup):
            filePipeline(pageSoup, linkTag, relativePath)
            print(linkTag.string)