import re
import sys
import urllib
from bs4 import BeautifulSoup

baseURL = "http://127.0.0.1:5000"
vulnerabilityCounter = 0
vulnerabilities = {}


def examineJavascriptForXSS(html, targetURL, inputField):
	return False  # temp value until function is actually implemented


def probeFoundXSSVulnerability(html, targetURL, inputField):
	return  # temp value until function is actually implemented


def probeFoundSQLiVulnerability(html, targetURL, inputField):
	return  # temp value until function is actually implemened


def examineForVulnerabilities(html, targetURL, element):
	pageExploits = {}
	print("Checking " + str(element) + " on page " + targetURL + " for XSS")
	if ".js" in str(element):
		print("Examining javascript code for XSS vulnerabilities")
		jsIsVulnerableToXSS = examineJavascriptForXSS(html, targetURL, element)
		if (jsIsVulnerableToXSS):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print(
			"XSS VULNERABILITY FOUND: " + str(element) + " on page " + targetURL + ". Javascript validation is broken.")
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL)
	else:
		print("Probing with sample input to test for XSS vulnerabilities")
		isVulnerable = probeFoundXSSVulnerability(html, targetURL, element)
		if (isVulnerable):
			pageExploits["XSS" + str(vulnerabilityCounter)] = str(element)
			vulnerabilityCounter += 1
			print("XSS VULERABILITY FOUND: " + str(element) + " on page " + targetURL + ". Found using probe-text: " + isVulnerable)
		else:
			print("No XSS vulnerabilities immediately found for " + str(element) + " on page " + targetURL)
			print("Probing with sample input to test for SQL-injection vulnerabilities")
			isVulnerable = probeFoundSQLiVulnerability(html, targetURL, element)
			if (isVulnerable):
				pageExploits["SQLi" + str(targetURL)] = str(element)
				vulnerabilityCounter += 1
				print("SQLi VULNERABILITY FOUND: " + str(
					element) + " on page " + targetURL + ". Found using probe-text: " + isVulnerable)
			else:
				print("No SQLi vulnerabilities immediately found for " + str(element) + " on page " + targetURL)
	return pageExploits

def probeTheWebsite(targetPage=['', 'login', 'register']):
	if (targetPage == ['', 'login', 'register']):
		print("No target URL extensions specified, defaulting to base list. Not likely to find much!!!!")
	for restOfURL in targetPage:
		targetURL = baseURL + '/' + restOfURL
		currentPageExploits = {}
		html = urllib.urlopen(targetURL).read()
		if (html):
			html = BeautifulSoup(html, "lxml")
			if "404" in html.text:
				print("Request for " + targetURL + " returned 404 error")
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
