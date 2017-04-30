import re
import sys
import urllib
from bs4 import BeautifulSoup

baseURL = "http://127.0.0.1:5000"

def probeTheWebsite(targetPage=['', 'login','register']) :

	vulnerabilities = {}
	writeBuffer = []
	if(targetPage == ['', 'login', 'register']) :
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!")
	for restOfURL in targetPage :
		targetURL = baseURL + '/' + restOfURL
		html = urllib.urlopen(targetURL).read()
		if(html) :
			html = BeautifulSoup(html, "lxml")
			if "404" in html.text :
				print("Request for " + targetURL + " returned 404 error")
				continue
			pageExploits = {}
			formFields = html.find_all('form')
			textAreas = html.find_all('textarea')
			for form in formFields :
				inputFields = form.find_all('input')
				for inputField in inputFields :
					print("Checking " + inputField.text + " on page " + targetURL + " for XSS")
					if ".js" in form.text :
						print("Examining javascript validation")
				# for each kind of XSS, check for XSS, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities

				# for each kind of SQL, check for SQL, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities
probeTheWebsite()
