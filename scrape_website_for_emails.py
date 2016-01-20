## given a list of websites, the scraper will look for email addresses on the page. 

import csv
import requests
import urllib,re
from bs4 import BeautifulSoup
from xlsxcessive.xlsx import Workbook, save


# with open('scraping_ny/scrape_education_cleaned.csv', 'rU') as f:
# 	s = csv.reader(f)
# 	schools = list(s)



emails = []

schools = ['website location']

def getWebsites(l):
	url = l
	try:
		r  = requests.get("http://"+url)
		data = r.text
		soup = BeautifulSoup(data)
		for link in soup.find_all('a'):
			site = link.get('href')
		# print site
			if site == None:
				site = url
			elif site[0] == "/":
				site_edit = "http://"+ url + site[1:]
				websites.append(site_edit)
			elif site != None:
				websites.append(site)
	except Exception as e:
	    print e.__doc__
	    print e.message
	    pass

	

def getEmails():
	try:
		print "--", row
		f = urllib.urlopen(row)
		s = f.read()
		print "WEBSITE CONTENT: ", s
		# a =  re.findall(r"\+\d{2}\s?0?\d{10}",s)
		b =  re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
		
		if len(b)>1:
			for r in b:
				if r not in emails:
					emails.append(r)
		elif len(b) == 1:
			if b[0] not in emails: 
				emails.append(b[0])
	except Exception as e:
	    print e.__doc__
	    print e.message
	    pass
	# except IOError:
	# 	pass

writer = csv.writer(open('scraping_ny/emails_ny.csv', 'wb'))
for s in schools:
	websites = []
	getWebsites(s[0])

	print "-" * 20
	print s[0]
	print "-" * 20

	print "WEBSITES::", len(websites)
	n = 1
	for row in websites:
		getEmails()
		n = n + 1

	print "-" * 20
	print "EMAILS::", len(emails)
	print " "

	for row in emails:
		print "-", row
		writer.writerow([row])

			
		
























