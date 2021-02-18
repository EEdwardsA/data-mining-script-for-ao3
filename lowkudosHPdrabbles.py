# -*- coding: utf-8 -*-
"""
Scraping tool for taking text from fanfics on AO3 and putting it into a text file.

"""

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time 

#---------------EDIT THIS CODE FOR SCRAPING OTHER FICS------------------------#
#given a start link - the first page of the tag with all the filters you want
page = "https://archiveofourown.org/works?utf8=%E2%9C%93&work_search%5Bsort_column%5D=kudos_count&include_work_search%5Brating_ids%5D%5B%5D=10&include_work_search%5Barchive_warning_ids%5D%5B%5D=16&include_work_search%5Bcategory_ids%5D%5B%5D=21&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=T&work_search%5Bwords_from%5D=50&work_search%5Bwords_to%5D=700&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=en&commit=Sort+and+Filter&tag_id=Harry+Potter+-+J*d*+K*d*+Rowling"
# NumberOfPages = 21 (used to be how many pages of results you wanted to scrape)


#--------------------Code for scraping AO3 fanfics----------------------------#
#make a list of all the pages that fit that tag limit list
def getPageList(startLink):
    links = [startLink]
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(startLink,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    olist = soup.find("ol", {"class": "pagination actions"}) #first, title navi
    lis = list(olist.find_all("li"))[-21:-1] #get the last 20 pages (originally said 0:NumberOfPages to get first x pages)
    for l in lis:
        try:
            a = l.find("a", href = True)['href'] 
            links.append(("https://archiveofourown.org" + a))
        except: pass
    return links
allPages = getPageList(page)

#Scrape, from each page, a link list of all the works on those pages
allFicList = []
def getPageFics(thisPage):
    thisFicList = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(thisPage,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    ols = soup.find("ol", {"class": "work index group"})
    lis = list(ols.find_all("li"))
    inlist = 0
    for l in lis:
        try:
            work = l.find("div", {"class": "header module"}).find("h4", {"class": "heading"}).find("a", href = True)['href']
            thisFicList.append(("https://archiveofourown.org" + work + "?view_full_work=true?view_adult=false"))
        except: 
            pass
    return thisFicList

for thisPage in allPages:
    allFicList.extend(getPageFics(thisPage))
#make sure they're all unique
allFicList = list(dict.fromkeys(allFicList))
print(len(allFicList))

#From each fic, take the body content and appeand onto a text file
def scrapedFics(fic):
    text = ""
    time.sleep(5) 
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(fic, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
        
    #about the actual text in the fiction
    # instead of creating a list of paragraphs, I need a new fi
    try:
        fiq = soup.find("div", {"class": "userstuff"})
        text = fiq.get_text().replace("<br/>", " ")
        # p = fiq.find_all("p")
        # for pp in p:
        #     text = pp.get_text().replace("<br/>", " ")
    except: 
        try: #fix it as though it were multichapter
            fiq = list(soup.find_all("div", {"class": "userstuff module"}))
            for f in fiq:
                # p = f.find_all("p")
                # for pp in p:
                text = fiq.get_text().replace("<br/>", " ")
        except: print("Error: ", fic)
    return text

count = 0

textt = ""
for fic in allFicList:
    print(count)
    nameOfFileCreated = f"../dep-story-squad-ds-b/notebooks/stories/story{count}.txt" #name of exported text file
    textFile = open(nameOfFileCreated, "a", encoding='utf8')
    textFile.write(scrapedFics(fic))
    count += 1
    textFile.close()