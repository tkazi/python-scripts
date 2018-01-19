## identify if a user is asking a question or looking for help in comments data (social netowring platform)

import os
import csv
import pandas as pd
from pandas import Series, DataFrame
from nltk.tokenize import sent_tokenize, word_tokenize

with open('test.csv', 'rU') as f:
    p = csv.reader(f)
    #next(p, None) 
    posts = list(p)

q = ['are','am','was','were','will','do','does','did','have','had','has','can','could','should','shall','may','might',
'would','what','what kind','what type','what sort','what time','what for','what like','when','why','where','who','how',
'how much','how many','how old','how far','how long','how fast','how often','how come','which','whom','whose','wherefore',
'whatever','wherewith','whither','whence','however','howcome','i am looking','i\'m looking', 'any', 'anyone', 'question','if']

def insertIntoDataStruct(community,posted_date,message, comments, aDict):
    if not community in aDict:
    	#print 'dict1', message
        aDict[community] = [(posted_date, message, comments)]
    else:
        #print 'dict2', message
        aDict[community].append((posted_date, message, comments))

results = {}
stage_results = []
for row in posts:
	try:
		sent_list = sent_tokenize(row[4].encode('utf-8'))
		for sent in sent_list:
			#print sent
			word_list = word_tokenize(sent)
			#print str(word_list[0]).lower()
			if str(word_list[0]).lower() in q:
				#print 'catch q', sent
				if row[4] not in stage_results:
					stage_results.append(row[4])
					#print 'staging', row[4]
					insertIntoDataStruct(row[2],row[0],row[4], row[3], results)
				#print row[1], "@", row[0]
			#print "-"
		#print "-----"
	except:
		pass

#print results
for key, value in results.iteritems():
    n = 1
    print key
    for row in value:
    	print str(n) + ') ', row[0], '('+str(row[2])+')', row[1]
    	print ''
    	n = n + 1
    print "--"*20

