## scrapes craigslist for new listings within a time period and other filter criteria. Any new listing found is emailed to the recipient.



#! /usr/local/bin/python

## to receive an email, enter email and password for your gmail account
gmail_user = 'johndoe@gmail.com'
gmail_password = 'pasword123'

recipient_email = [''] ## this is an array, keep brackets around the quotes. also can add multiple recipients. for example: ['taha@gmail.com','adam@gmail.com']

minRentPrice = 2500
maxRentPrice = 5000
numberBedrooms = 4

# southbay: http://sfbay.craigslist.org/search/sby/apa
# peninsula: http://sfbay.craigslist.org/search/pen/apa
# san fran city: http://sfbay.craigslist.org/search/sfc/apa

craigslist_url = 'http://sfbay.craigslist.org/search/sfc/apa'


### above this line are all the params needed for scarping

import re
import sys
import datetime
import requests
import smtplib
import mimetypes
from bs4 import BeautifulSoup
# from premailer import transform
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

now = datetime.datetime.now()

month = now.month
day = now.day
hour = now.hour
minute = now.minute

print str(month) + "/" + str(day) + " - " + str(hour) + ":" + str(minute)

def fetch_search_results(
    query=None, minAsk=None, maxAsk=None, bedrooms=None
):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = craigslist_url

    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    return resp.content, resp.encoding

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

def extract_listings(parsed):
    listings = parsed.find_all('p', class_='row')
    #print len(listings)
    return listings

def get_link(listing):
    soup = BeautifulSoup(listing)
    #find if listing has a picture
    listing_with_pic = str(soup.findAll('span', attrs={'class':'p'}))
    
    find_price = str(soup.findAll('span', attrs={'class':'price'}))
    price =  find_price[21:26]

    find_title = soup.findAll('a')
    #print len(find_title)
    if len(find_title) > 1:
        soup_title = str(find_title[1])
        soup2 = BeautifulSoup(soup_title)
        # print len(soup2.a.contents)
        if soup2.a:
            #print price, soup2.a.contents[0]
            title = soup2.a.contents[0]

    if len(listing_with_pic) > 0:
        pic =  listing_with_pic[18:21]
    
    date_present = re.findall("datetime",listing)
    #find time of the listing
    if date_present:
        listing_time = str(soup.time['datetime'])
        listing_month = int(listing_time[5:7])
        listing_day = int(listing_time[8:10])
        listing_hour = int(listing_time[11:13])
        listing_minute = int(listing_time[14:16])
        
        new_site = ''
        region = ''
        for link in soup.find_all('a'):
            #print link
            #print listing_month
            if pic == 'pic' and listing_month == month and listing_day == day and listing_hour in [hour, hour-1, hour-2]:
                site = link.get('href')
                #print site
                if site:
                    #print site[27:31]
                    if site[:8] == '/sfc/apa':
                        new_site = "http://sfbay.craigslist.org" + str(site)
                        region = 'South Bay'           
                    if site[:7] == '//sfbay':
                        #site = "http://sfbay.craigslist.org" + str(site)
                        site = "http:" + str(site)
                    if new_site or site not in links:
                        #print site
                        price_title = price + " " + title + " - (" + region + ")"
                        titles.append(price_title)
                        if new_site:
                            links.append(new_site)
                        if site:
                            links.append(site)
                        prices.append(price)



links = []
titles = []
prices = []

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(
            minAsk=minRentPrice, maxAsk=maxRentPrice, bedrooms=numberBedrooms
        )
    doc = parse_source(html, encoding)
    #print doc.prettify(encoding=encoding)
    listings = extract_listings(doc)
    for listing in listings:
        if listing:
            get_link(str(listing))

listings_dict = dict(zip(titles, links))

p_tag = ''
for key, value in listings_dict.iteritems():
    #print value
    p_tag += '<div class="listing">'
    p_tag += '<p><a target="_blank" href="' + str(value.encode('utf-8')) + '">' + str(key.encode('utf-8')) + '</a></p>'
    p_tag += '</div>'
#print p_tag


## email 
heading = ''
if len(listings_dict) == 0:
    heading = '0 listing posted in the previous hour'
else:
    heading = str(len(listings_dict)) + ' post(s) in the last hour'
    #email
    emailfrom = "craigslist scraper"
    recipients = recipient_email
    user = gmail_user
    password = gmail_password

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(recipients)
     
    msg["Subject"] = "Craigslist Listings " + str(month) + "/" + str(day) + " - " + str(hour) + ":" + str(minute)

    html = """
                <html>
                  <head>
                  <style>
                    body, html {margin:0; padding:0; width:100%;}
                    div {text-align:center; margin:0 auto; margin-bottom:20px; width:620px;}
                    h4{background: rgb(223, 80, 61); width: 275px; margin: 0 auto; padding: 8px 5px; 
                      border-radius: 4px; margin-bottom: 20px; color: white; text-align:center;}
                    p {padding:10px 5px; margin:0; width:90%; border:1px solid #eee; border-radius:4px; margin:0 auto;}
                    a { text-decoration: none; border-radius:4px;}
                    @media screen 
                    and (min-device-width : 375px) 
                    and (max-device-width : 667px) { a, p {font-size:12px;} h4{margin-top:20px; font-size:12px;}}
                  </style>
                  </head>
                  <body>
                  <h4>""" + heading + """</h4> 
                   """ + p_tag + """ 
                  </body>
                </html>
                """
    #print html
    html = MIMEText(html, 'html')

    msg.attach(html)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(user,password)
    server.sendmail(emailfrom, recipients, msg.as_string())
    server.quit()





