from bs4 import BeautifulSoup
from random import uniform
import urllib2 
import time
import csv
import os
import re
import codecs

f=codecs.open('C:\Users\ststest\Dropbox\TextAnalysis Grimmer\Day1\Debate1.html','r')
deb=f.read()
soup=BeautifulSoup(deb)

####EXERCISE 1

#To identify tags
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print "<%s>"%tag
	def handle_endtag(self, tag):
		print "</%s>"%tag

parser = MyHTMLParser();
parser.feed(deb)
#Tags: head, title, link, body, div, a, p, and script.

#Restricting to the statements of the debate
soup2=soup.find_all('p')[6:477]

#Prints statements starting with OBAMA
#for st in soup2:
#	if 'OBAMA' in st.string:
#		print st.string

#Assigning unlabeled statements to speakers and filter out notes from audience
sts=list()
for idx, st in enumerate(soup2):
	#print(idx, st.string)
	if re.match(r'^([A-Z]*:)',st.string):
		sts.append(st.string)
		subj=re.search(r'^^([A-Z]*:)',st.string).group(0)
	else:
		if re.match(r'\([A-Z].*[A-Z]\)', st.string): #This cleans audience notes
			pass
		else:
			sts.append(subj+st.string) #This adds classifier to unlabeled statements

for st in sts:
	print st

#Final step is to append multiple statements by the same guy to a single string
final=list()
final.append(sts[0])
#final[len(final)-1] give the last element of final
for st in sts[1:len(sts)]:
	authorprev=re.search(r'^[A-Z]*:', final[len(final)-1]).group(0)
	authornow=re.search(r'^[A-Z]*:', st).group(0)
	if authorprev==authornow:
		addon=re.sub(r'^[A-Z]*:','',st)
		final[len(final)-1]=final[len(final)-1]+' '+str(addon)
	else:
		final.append(st)

#Finally:		
for st in final:
	print str(st)
	

	
####EXERCISE 2
import nltk
#nltk.download('punkt')
from urllib import urlopen
from nltk import word_tokenize
pos_words = urlopen('http://www.unc.edu/~ncaren/haphazard/positive.txt').read().split('\n')
neg_words = urlopen('http://www.unc.edu/~ncaren/haphazard/negative.txt').read().split('\n')
stop_words = urlopen('http://jmlr.org/papers/volume5/lewis04a/a11-smart-stop-list/english.stop').read().split('\n')

#PORTER
from nltk.stem import PorterStemmer
pt = PorterStemmer()
pos_stem_pt=map(pt.stem,pos_words)
neg_stem_pt=map(pt.stem,neg_words)

#from collections import Counter
#len(Counter(pos_stem_pt))
#len(Counter(neg_stem_pt))

#SNOWBALL
from nltk.stem.snowball import EnglishStemmer
sb = EnglishStemmer()
pos_stem_sb=map(sb.stem,pos_words)
neg_stem_sb=map(sb.stem,neg_words)

#LANCASTER
from nltk.stem.lancaster import LancasterStemmer
lc = LancasterStemmer()
pos_stem_lc=map(lc.stem,pos_words)
neg_stem_lc=map(lc.stem,neg_words)


#Simplifying text and creating stemmed databases
debate=list()
debate_pt=list()
debate_lc=list()
debate_sb=list()
for st in final:
	text_1 = st.lower()
	text_2 = re.sub('\W', ' ', text_1)
	text_3 = word_tokenize(text_2)
	text_4 = [x for x in text_3 if x not in stop_words]
	debate.append(text_4)
	debate_lc.append(map(lc.stem,text_4))
	debate_pt.append(map(pt.stem,text_4))
	debate_sb.append(map(sb.stem,text_4))

	
#Last Step
with open('test2.csv', 'wb') as f:
  my_writer = csv.DictWriter(f, fieldnames=("ID", "speaker", 'non-stop','pos','neg','lc_pos','lc_neg','pt_pos','pt_neg','sb_pos','sb_neg'))
  my_writer.writeheader()
  for i in range(1, len(final)):
	person=re.search(r'^[A-Z]*:', str(final[i-1])).group(0)[0:-1] #subject	
	pwords=len([e for e in debate[i-1] if e in pos_words]) #pos
	nwords=len([e for e in debate[i-1] if e in neg_words]) #neg
	pos_lc = len([x for x in debate_lc[i-1] if x in pos_stem_lc]) #pos lancaster
	neg_lc = len([x for x in debate_lc[i-1] if x in neg_stem_lc]) #neg lancaster
	pos_pt = len([x for x in debate_pt[i-1] if x in pos_stem_pt]) #pos porter
	neg_pt = len([x for x in debate_pt[i-1] if x in neg_stem_pt]) #neg porter
	pos_sb = len([x for x in debate_sb[i-1] if x in pos_stem_sb]) #pos snowball
	neg_sb = len([x for x in debate_sb[i-1] if x in neg_stem_sb]) #neg snowball
	my_writer.writerow({"ID":i, 'speaker':person, 'non-stop':len(debate[i-1]), 'pos':pwords, 'neg':nwords, 'pt_pos':pos_pt, 'pt_neg':neg_pt, 'lc_pos':pos_lc, 'lc_neg':neg_lc, 'sb_pos':pos_sb, 'sb_neg':neg_sb})

