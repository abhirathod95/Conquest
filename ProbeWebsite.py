import requests
import random
import vuln_page
from prompt import hack
from bs4 import BeautifulSoup

vulnerabilities = []
vulnerabilityCounter = 0
loginPage = None
SQLiTexts = ["Wayne\'s World", 'Wayne\"s World', "\' OR 1=1;--", "\" OR 1=1;--"]

def examineJavascriptForXSS(html, targetURL, inputField, session):
	return False  # temp value until function is actually implemented

def cleanVulnerabilities() :
	global vulnerabilities
	tempVulnerabilities = {}
	v = vulnerabilities.copy()
	for vulnerability in v :
		string = vulnerability.vuln[0]		#TODO if time permit
		string += vulnerability.url
		string += str(vulnerability.req_type)
		try :
			if tempVulnerabilities[string]:
				vulnerabilities.remove(vulnerability)
			else :
				tempVulnerabilities[string] = 1
		except :
				tempVulnerabilities[string] = 1

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
	data = {"body" : probeText, "placeholder" : probeText, "text" : probeText, "title" : probeText, "user" : probeText, "username" : probeText, "password": probeText, "pass" : probeText, "pw" : probeText, "entry" : probeText, "entry_add" : probeText, "blog" : "add", "action" : "search"}
	try :
		if("sqli" in targetURL) :
			return
		session.post(targetURL, data)
		html = session.get(targetURL)
		html = BeautifulSoup(html.text, "html.parser")
		successfulText = locateScriptTagsWithString(html, baseString)
		if(successfulText) :
			nameOfPage = targetURL.split("/")
			length = len(nameOfPage)
			nameOfPage = nameOfPage[length-1]
			vuln = vuln_page.VulnPage(nameOfPage, targetURL, ["XSS"], data, 1, 0)
			vulnerabilities.append(vuln)
			return successfulText
	except :
		return

def checkIfSQLi(html, forcedLogin=False) :
	htmlPage = html.text
	error = "error" in htmlPage or "ERROR" in htmlPage or "Error" in htmlPage or "err" in htmlPage or "ERR" in htmlPage or "Err" in htmlPage
	sql = "sql " in htmlPage or " SQL" in htmlPage or "Sql " in htmlPage
	grammar = "syntax" in htmlPage or "Syntax" in htmlPage or "SYNTAX" in htmlPage or "statement" in htmlPage or "Statement" in htmlPage or "STATEMENT" in htmlPage

	if(error and sql and grammar) :				# checks for defacto SQLi information leak. If true, then there's a SQL vulnerability.
		return True

	if("Error: HY000" in htmlPage) :
		return True

	if(forcedLogin) :
		logOut = "log out" in htmlPage or "Log Out" in htmlPage or "LOG OUT" in htmlPage or "Log OUT" in htmlPage or "log OUT" in htmlPage
		signOut = "sign out" in htmlPage or "Sign Out" in htmlPage or "SIGN OUT" in htmlPage or "Sign OUT" in htmlPage or "sign OUT" in htmlPage
		if(logOut or signOut) :
			return True
		else :
			successful = "success" in htmlPage or "SUCCESS" in htmlPage
			registered = "registered" in htmlPage or "Registered" in htmlPage or "Registration" in htmlPage or "registration" in htmlPage
			if(successful and registered) :
				return True
	return False

def probeFoundSQLiVulnerability(html, targetURL, inputField, session) :
	for probeText in SQLiTexts :
		try :
			data = {"username": probeText, "login" : probeText, "email" : probeText, "email_address" : probeText, "emailAddress" : probeText, "password": probeText, "name": probeText, "firstname": probeText, "first": probeText, "last": probeText, "fname": "'", "lname": probeText, "entry" : probeText, "blog" : "add", "form" : "submit"}
			html = session.post(targetURL, data)
			if(html.status_code == 400 or html.status_code == 404 or html.status_code == 403 or html.status_code == 405) :
				raise Exception
			# html = BeautifulSoup(html.text, "html.parser")
			if(probeText == SQLiTexts[2] or probeText == SQLiTexts[3]) :
				vulnerable = checkIfSQLi(html, True)
			else :
				vulnerable = checkIfSQLi(html)
			if(vulnerable) :
				nameOfPage = targetURL.split("/")
				length = len(nameOfPage)
				nameOfPage = nameOfPage[length - 1]
				if("\'" in probeText) :
					symbol = 0
				else :
					symbol = 1
				vuln = vuln_page.VulnPage(nameOfPage, targetURL, ["SQL"], data, 1, symbol)
				vulnerabilities.append(vuln)
				return probeText
			else :
				raise Exception
		except :
			try :
				name = inputField.attrs['name']
				queryURL = targetURL + "?" + name + "=" + probeText
				if ("sqli" in targetURL):
					queryURL += "&action=search"
				html = session.get(queryURL)
				html = BeautifulSoup(html.text, "html.parser")
				vulnerable = checkIfSQLi(html)
				if(vulnerable) :
					nameOfPage = targetURL.split("/")
					length = len(nameOfPage)
					nameOfPage = nameOfPage[length - 1]
					if("\'" in probeText):
						symbol = 0
					else:
						symbol = 1
					vuln = vuln_page.VulnPage(nameOfPage, targetURL, ["SQL"], {name : probeText}, 0, symbol)
					vulnerabilities.append(vuln)
					return probeText
			except :
				return
	return

def examineForVulnerabilities(html, targetURL, element, session):
	global vulnerabilityCounter
	pageExploits = {}
	if ".js" in str(element):
		jsIsVulnerableToXSS = examineJavascriptForXSS(html, targetURL, element, session)
		if (jsIsVulnerableToXSS):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print("XSS VULNERABILITY FOUND: " + str(element) + " on page " + targetURL)
		else:
			print("No XSS vulnerabilities immediately found for page " + targetURL)
	else:
		isVulnerable = probeFoundXSSVulnerability(html, targetURL, element, session)
		if (isVulnerable) :
			vulnerabilityCounter += 1
			print("XSS VULERABILITY FOUND:  " + str(element) + "  on page " + targetURL + " . Found using probe-text:  " + isVulnerable)
		else:
			print("No XSS vulnerabilities immediately found for page " + targetURL)
			isVulnerable = probeFoundSQLiVulnerability(html, targetURL, element,	session)
			if(isVulnerable) :
				vulnerabilityCounter += 1
				print("SQLi VULNERABILITY FOUND:  " + str(element) + " on page " + targetURL + " . Found using probe-text:  " + isVulnerable)

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
			loginPage = targetURL
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
			if html.status_code == 404:
				print("Request for " + targetURL + " returned 404 error\n")
				continue
			html = BeautifulSoup(html.content, "html.parser")
			formFields = html.find_all('form')
			for form in formFields :
				inputFields = form.find_all('input')
				textAreas = form.find_all('textarea')
				for inputField in inputFields:
					examineForVulnerabilities(html, targetURL, inputField, session)
				for textArea in textAreas:
					examineForVulnerabilities(html, targetURL, textArea, session)

	cleanVulnerabilities()
	vulnerabilityCounter = len(vulnerabilities)
	if(vulnerabilityCounter == 0):
		print("No vulnerabilities found.\n")
	else :
		if(vulnerabilityCounter == 1):
			print("1 vulnerability found!\n")
		else :
			print(str(len(vulnerabilities)) + " vulnerabilities found!\n")

	hack(loginPage, vulnerabilities, session)
