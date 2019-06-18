import urllib
import time
from bs4 import BeautifulSoup
import re
import sys

def check_philosophy(url, articles_set):
    if url in articles_set:
        #if url was visited before then we entered a loop
        print("Entered a loop")
        return False,None
    articles_set[url]=1
    try:
        html_page = urllib.request.urlopen(url)
        parser = BeautifulSoup(html_page, 'html.parser')
    except:
        #connection error occured
        print("An error occured")
        return False, None
    heading=parser.find(id="firstHeading")
    if heading.text=="Philosophy":#check if the title of the article is Philosophy
        print("Philosophy reached!")
        return False,None
    for match in parser.findAll('b'):
        match.unwrap()
    main_article=parser.find("div",class_="mw-parser-output")
    links=parser.select("div[class=mw-parser-output] > p > a")#select links that are direct children of p tag to avoid table and italics
    if len(links)<1:
        links=parser.select("div[class=mw-parser-output] > ul > a")
    for link in links:

        if str(link.attrs['href']).startswith('#') or 'class' in link.attrs\
                or re.findall('\([^\(\)]*'+str(link)+'[^\(\)]*\)',str(main_article)).__len__()>0:
            #all links inside brackets,linking to the same page or red links are discarded
            #normal links have no class
            continue
        return True,"https://en.wikipedia.org"+link.attrs['href']
    print("Last page without links")
    return False,None


if __name__ == "__main__":
    scrape=True
    articles_set={}
    if len(sys.argv) == 1:
        url="http://en.wikipedia.org/wiki/Special:Random"
    else:
        url=sys.argv[1]
    while scrape:
        scrape,url=check_philosophy(url, articles_set)
        time.sleep(0.5)
    for url in articles_set.keys():
        print(url)