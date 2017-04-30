import urllib
from bs4 import BeautifulSoup

baseURL = "http://127.0.0.1:5000"
vulnerabilities = {}
vulnerabilityCounter = 0


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
	html2 = urllib.urlopen(queryURL).read()
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
			print("Probing with sample input to test for SQL-injection vulnerabilities\n")
			isVulnerable = probeFoundSQLiVulnerability(html, targetURL, element)
			if (isVulnerable):
				pageExploits["SQLi" + str(targetURL)] = str(element)
				vulnerabilityCounter += 1
				print("SQLi VULNERABILITY FOUND: " + str(element) + " on page " + targetURL + ". Found using probe-text: " + isVulnerable + "\n")
			else:
				print("No SQLi vulnerabilities immediately found for " + str(element) + " on page " + targetURL + "\nEither element is not vulnerable, or website is good about not leaking information.\n")
	return pageExploits

def probeTheWebsite(targetPage=['', 'login', 'register', 'movies']):
	global vulnerabilities
	if (targetPage == ['', 'login', 'register', 'movies']):
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!\n\n")
	for restOfURL in targetPage:
		targetURL = baseURL + '/' + restOfURL
		currentPageExploits = {}
		html = urllib.urlopen(targetURL).read()
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
		print(str(vulnerabilityCounter) + " vulnerabilities found!\n")
				# for each kind of XSS, check for XSS, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities

				# for each kind of SQL, check for SQL, store in file buffer, print to screen, and if vulnerable, add to vulnerabilities


probeTheWebsite()
