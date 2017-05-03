import requests
import random
from bs4 import BeautifulSoup

vulnerabilities = {}
vulnerabilityCounter = 0
loginPage = []

def examineJavascriptForXSS(html, targetURL, inputField, session):
	return False  # temp value until function is actually implemented

def locateScriptTagsWithString(html, stringToFind) :
	filtered = (stringToFind not in html.text) or ((stringToFind + "<script></script>") in html.text)
	if(filtered):
		return
	kindsOfTags = ["li", "text", "td", "tr", "p"]
	for tag in kindsOfTags :
		elements = html.find_all(tag)
		if stringToFind not in str(elements) :
			continue
		theCorrectElement = elements[0]
		for element in elements :
			if(stringToFind in str(element)) :
				theCorrectElement = element
				if(stringToFind + "<script></script>" in str(element.contents)) :
					return (stringToFind + "<script></script>")
				# find out if this element has script tags associated with it
	return

def probeFoundXSSVulnerability(html, targetURL, inputField, session) :
	randomNumber = random.randint(5599993912, 2459510340230403407)
	baseString ="I really really x" + str(randomNumber) + " times like this"
	probeText = baseString + "<script></script>"
	data = {"body" : probeText, "placeholder" : probeText, "text" : probeText, "user" : probeText, "username" : probeText, "password": probeText, "pass" : probeText, "pw" : probeText}
	try :
		session.post(targetURL, data)
		html = session.get(targetURL)
		html = BeautifulSoup(html.text, "html.parser")
		successfulText = locateScriptTagsWithString(html, baseString)
		if(successfulText) :
			return successfulText
	except :
		return

def checkIfSQLi(html) :
	htmlPage = html.prettify()
	error = "error" in htmlPage or "ERROR" in htmlPage or "Error" in htmlPage or "err" in htmlPage or "ERR" in htmlPage or "Err" in htmlPage
	sql = "sql" in htmlPage or "SQL" in htmlPage or "Sql" in htmlPage
	grammar = "syntax" in htmlPage or "Syntax" in htmlPage or "SYNTAX" in htmlPage or "statement" in htmlPage or "Statement" in htmlPage or "STATEMENT" in htmlPage

	if(error and sql and grammar) :				# checks for defacto SQLi information leak. If true, then there's a SQL vulnerability.
		return True

	return False

def probeFoundSQLiVulnerability(html, targetURL, inputField, session) :
	probeText1 = "Wayne's World"
	data = {"username" : "'", "password" : "'", "name" : "'", "firstname" : "'", "first" : "'", "last" : "'", "fname" : "'", "lname" : "'"}

	try :
		probeText = probeText1
		html = session.post(targetURL, data)
		if("405" in html.text or "403" in html.text or "400" in html.text) :
			raise Exception
		html = BeautifulSoup(html.text, "html.parser")
		vulnerable = checkIfSQLi(html)
		if(vulnerable) :
			return probeText
	except :
		try :
			probeText = probeText1
			name = inputField.attrs['name']
			queryURL = targetURL + "?" + name + "=" + probeText
			html = session.get(queryURL)
			html = BeautifulSoup(html.text, "html.parser")
			vulnerable = checkIfSQLi(html)
			if(vulnerable) :
				return probeText
		except :
			return
	return

def examineForVulnerabilities(html, targetURL, element, session):
	global vulnerabilityCounter
	pageExploits = {}
	print("Checking " + str(element) + " on page " + targetURL + " for XSS\n")
	if ".js" in str(element):
		print("Examining javascript code for XSS vulnerabilities\n")
		jsIsVulnerableToXSS = examineJavascriptForXSS(html, targetURL, element, session)
		if (jsIsVulnerableToXSS):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print("XSS VULNERABILITY FOUND: " + str(element) + " on page " + targetURL + " . Javascript validation is broken.\n")
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL + "\nEither element is not vulnerable, or website is good about not leaking information.\n	")
	else:
		print("Probing with sample input to test for XSS vulnerabilities\n")
		isVulnerable = probeFoundXSSVulnerability(html, targetURL, element, session)
		if (isVulnerable) :
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print("XSS VULERABILITY FOUND: \" " + str(element) + " \" on page " + targetURL + " . Found using probe-text: \" " + isVulnerable + " \"\n")
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL + "\nEither element is not vulnerable, or website is good about not leaking information.\n")
			print("Probing with sample input to test for SQLi vulnerabilities\n")
			isVulnerable = probeFoundSQLiVulnerability(html, targetURL, element,	session)
			if(isVulnerable) :
				pageExploits["SQLi" + str(vulnerabilityCounter)] = str(element)
				vulnerabilityCounter += 1
				print("SQLi VULNERABILITY FOUND: \" " + str(element) + "\" on page " + targetURL + " . Found using probe-text: \" " + isVulnerable + " \"\n")

	return pageExploits


def probeTheWebsite(baseURL="http://127.0.0.1:5000", targetPage=['/', '/login', '/register', '/movies', '/forum'], authenticatedSession=None):
	global vulnerabilities
	session = None
	if (not targetPage) :
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!\n\n")
		targetPage = ['/', '/login', '/register', '/movies', '/forum']

	if (authenticatedSession):
		session = authenticatedSession
		print("Passed an authenticated session! Trying all pages.\n")
	else:
		session = requests.Session()
		print("Passed in an unauthenticated session. Trying all pages that don't require authentication. Results may be LIMITED.\n")
	for restOfURL in targetPage :
		targetURL = baseURL + restOfURL
		if("login" in restOfURL) :
			loginPage.append(targetURL)
		currentPageExploits = {}
		try :
			html = session.get(targetURL)
		except :									# if html gets a 401 unauthorized error
			print("Cannot get to this page without authorization. Obtain an account with proper authorization and rerun this program.")
			if(authenticatedSession) :
				# data = urllib.urlencode({"email" : authorization[0], "password" : authorization[1]})
				# urllib.urlopen(baseURL + "/login", data)
				try :
					# session = some kind of authorized session
					html = session.get(targetURL)
				except :
					print("Credentials were not valid, or another problem happened after attempting to authenticate for URL: " + targetURL)
					continue
		if (html):
			html = BeautifulSoup(html.content, "html.parser")
			if "404" in html.text:
				print("Request for " + targetURL + " returned 404 error\n")
				continue
			formFields = html.find_all('form')
			for form in formFields :
				inputFields = form.find_all('input')
				textAreas = form.find_all('textarea')
				for inputField in inputFields:
					currentPageExploits.update(examineForVulnerabilities(html, targetURL, inputField, session))
				for textArea in textAreas:
					currentPageExploits.update(examineForVulnerabilities(html, targetURL, textArea, session))

	vulnerabilities[targetURL] = currentPageExploits
	if(vulnerabilityCounter == 0):
		print("No vulnerabilities found.\n")
	else :
		if(vulnerabilityCounter == 1):
			print("1 vulnerability found!\n")
		else :
			print(str(vulnerabilityCounter) + " vulnerabilities found!\n")
	#
