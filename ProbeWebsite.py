import re
import sys
import urllib
from bs4 import BeautifulSoup

baseURL = "http://127.0.0.1:5000"

def probeTheWebsite(targetPage=['', 'login','register']) :
	if(targetPage == ['', 'login', 'register']) :
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!")
	for restOfURL in targetPage :
		targetURL = baseURL + '/' + restOfURL
		html = urllib.urlopen(targetURL).read()
		if(html) :
			html = BeautifulSoup(html, "lxml")
			print(html)	

probeTheWebsite()
