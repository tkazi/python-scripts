# from a list of districts provided, automate google search and download related documents

import urllib
import mechanize
import re
import requests
from bs4 import BeautifulSoup


def searchGoogle(link):
    keyword = link
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent','chrome')]

    term = keyword.replace(" ","+")
    query = "http://www.google.com/search?num=10&q="+term
    htmltext = br.open(query).read()
    soup = BeautifulSoup(htmltext)
    search = soup.findAll('div', attrs={'id':'search'})
    # print search
    searchtext = str(search[0])
    soup1 = BeautifulSoup(searchtext)
    list_items = soup1.findAll('li')
    #print list_items[0]
    regex = "q(?!.*q).*?&amp"
    pattern = re.compile(regex)

    results = []
    for li in list_items:
        soup2 = BeautifulSoup(str(li))
        links = soup2.findAll('a')
        source_link = links[0]
        #print "source link:", source_link
        source_url = re.findall(pattern, str(source_link))
        #print len(source_url[0])
        if len(source_url) > 0:
            #print source_url
            if len(source_url[0]) > 5:
                link = source_url[0].replace("q=","").replace("&amp","")
                #print link
                if (link[:12] == 'related:http' or link[:12] == 'related:www.'):
                    new_link = link.replace("related:","").replace("+"+str(term),"")
                    if new_link not in results:
                        results.append(new_link)
                if (len(link) > 5 and link[:4] == 'http'):
                    if link not in results:
                        results.append(link)
    for row in results:
        print row
    return results


districts = ['orange county schools florida']

for item in districts:
    print ""
    print "------", item, "------"
    results_2 = searchGoogle(item)
    print ""
















