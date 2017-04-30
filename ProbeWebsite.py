import urllib2
import urllib
from bs4 import BeautifulSoup

baseURL = "http://127.0.0.1:5000"
vulnerabilities = {}
vulnerabilityCounter = 0



def credentials(url, username, password):				# this code provided freely by the helpful contributors at http://stackoverflow.com/questions/40221579/http-error-401-unauthorized-using-urllib-request-urlopen
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

def examineJavascriptForXSS(html, targetURL, inputField):
	return False  # temp value until function is actually implemented


def probeFoundXSSVulnerability(html, targetURL, inputField):
	return  # temp value until function is actually implemented


def probeFoundSQLiVulnerability(html, targetURL, inputField):
	probeText = "'"
	name = inputField.attrs['name']
	id = str(inputField.attrs['id'])
	placeholder = str(inputField.attrs['placeholder'])
	isSearchQuery = False
	if(placeholder and id) :
		isSearchQuery = 'results' in placeholder or 'Results' in placeholder or 'RESULTS' in placeholder
		isSearchQuery = isSearchQuery or 'search' in placeholder or 'Search' in placeholder or 'SEARCH' in placeholder
		isSearchQuery = isSearchQuery or 'find' in placeholder or 'Find' in placeholder or 'FIND' in placeholder
		isSearchQuery = isSearchQuery or 'search' in id or 'Search' in id or 'SEARCH' in id
	queryURL = targetURL + "?" + name + "=" + probeText
	html2 = urllib2.urlopen(queryURL).read()
	if(html2) :
		html2 = BeautifulSoup(html2, "lxml")
		tableEntries = html2.find_all('td')
		noEntries = tableEntries.__len__() == 0
		brokeQuery = True
		if(not noEntries) :
			for entry in tableEntries :
				brokeQuery = brokeQuery and ("NA" in str(entry) or "N/A" in str(entry))
		if (noEntries or brokeQuery) and isSearchQuery :
			return probeText
		else :
			containsError = "error" in html2.text or "Error" in html2.text or "ERROR" in html2.text
			containsSQL = "syntax" in html2.text or "Syntax" in html2.text or "SYNTAX" in html2.text
			containsSQL = containsSQL or "sql" in html2.text or "SQL" in html2.text or "Sql" in html2.text
			containsSQL = containsSQL or "query" in html2.text or "Query" in html2.text or "QUERY" in html2.text
			if(containsError and containsSQL) :
				return probeText
	else :
		pass

	return

def examineForVulnerabilities(html, targetURL, element):
	global vulnerabilityCounter
	pageExploits = {}
	print("Checking " + str(element) + " on page " + targetURL + " for XSS\n")
	if ".js" in str(element):
		print("Examining javascript code for XSS vulnerabilities\n")
		jsIsVulnerableToXSS = examineJavascriptForXSS(html, targetURL, element)
		if (jsIsVulnerableToXSS):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print(
			"XSS VULNERABILITY FOUND: " + str(element) + " on page " + targetURL + ". Javascript validation is broken.\n")
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL + "\nEither element is not vulnerable, or website is good about not leaking information.\n	")
	else:
		print("Probing with sample input to test for XSS vulnerabilities\n")
		isVulnerable = probeFoundXSSVulnerability(html, targetURL, element)
		if (isVulnerable):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print("XSS VULERABILITY FOUND: " + str(element) + " on page " + targetURL + ". Found using probe-text: " + isVulnerable + "\n")
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL + "\nEither element is not vulnerable, or website is good about not leaking information.\n")

	return pageExploits

def probeTheWebsite(authorization=None, targetPage=['', 'login', 'register', 'movies', 'forum']):
	authorization = ('a', 'a')		# need to remove this after integrating with rest of project

	global vulnerabilities
	if (targetPage == ['', 'login', 'register', 'movies']):
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!\n\n")
	for restOfURL in targetPage:
		targetURL = baseURL + '/' + restOfURL
		currentPageExploits = {}
		if(authorization) :
			credentials(targetURL, authorization[0], authorization[1])
		try :
			html = urllib2.urlopen(targetURL).read()
		except :									# if html gets a 401 unauthorized error
			print("Cannot get to this page without authorization. Register for an account and rerun this method and pass this credentials as the first parameter. Ex: probeTheWebsite((username, password), targetURLs)")
			if(authorization) :
				# data = urllib.urlencode({"email" : authorization[0], "password" : authorization[1]})
				# urllib.urlopen(baseURL + "/login", data)
				try :
					html = urllib2.urlopen(targetURL).read()
				except :
					print("Credentials were not valid, or another problem happened after attempting to authenticate for URL: " + targetURL)
		if (html):
			html = BeautifulSoup(html, "lxml")

			if "404" in html.text:
				print("Request for " + targetURL + " returned 404 error\n")
				continue
			formFields = html.find_all('form')
			for form in formFields :
				inputFields = form.find_all('input')
				textAreas = form.find_all('textarea')
				for inputField in inputFields:
					currentPageExploits.update(examineForVulnerabilities(html, targetURL, inputField))
				for textArea in textAreas:
					currentPageExploits.update(examineForVulnerabilities(html, targetURL, textArea))
		vulnerabilities[targetURL] = currentPageExploits
				# for each kind of XSS, check for XSS, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities

				# for each kind of SQL, check for SQL, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities


probeTheWebsite()
print(str(vulnerabilityCounter) + " vulnerabilities found!\n")
