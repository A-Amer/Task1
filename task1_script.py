import urllib
import time
from bs4 import BeautifulSoup
import re

def get_content(url,articles_set):
    if url in articles_set:
        return False,None
    articles_set[url]=1
    html_page=None
    try:
        html_page = urllib.request.urlopen(url)
    except:
        print("An error occured")

    parser= BeautifulSoup(html_page, 'html.parser')
    heading=parser.find(id="firstHeading")
    if heading.text=="Philosophy":
        return False,None
    for match in parser.findAll('b'):
        match.unwrap()
    main_article=parser.find("div",class_="mw-parser-output")
    links=parser.select("div[class=mw-parser-output] > p > a")
    if len(links)<1:
        links=parser.select("div[class=mw-parser-output] > ul > a")
    for link in links:

        if str(link.attrs['href']).startswith('#') or 'class' in link.attrs or re.findall('\([^\(\)]*'+str(link)+'[^\(\)]*\)',str(main_article)).__len__()>0:
            continue
        return True,"https://en.wikipedia.org"+link.attrs['href']
    return False,None

scrape=True
articles_set={}
url="https://en.wikipedia.org/wiki/Science"
while scrape:
    scrape,url=get_content(url,articles_set)
    time.sleep(0.5)
for url in articles_set.keys():
    print(url)