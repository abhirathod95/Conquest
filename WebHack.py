import sys
import httplib2
import argparse

from bs4 import BeautifulSoup, SoupStrainer

import requests
import ProbeWebsite

existingPages = []
alreadySpidered = []

s = requests.session()

def spider():
	print('begin spider. ' + str(existingPages))
	while set(existingPages) != set(alreadySpidered):
		for page in existingPages:
			print('spidering page: '+page)
			if page not in alreadySpidered:
				resp = s.get(baseURL + page, allow_redirects=False).content
				print('spidering: '+page)
				alreadySpidered.append(page)
				for spiderLink in BeautifulSoup(resp, "html.parser", parse_only=SoupStrainer('a')):
					if spiderLink.has_attr('href') and (spiderLink['href'] not in existingPages) and ('/' + spiderLink['href'] not in existingPages):
						spiderLink = spiderLink['href']
						if ('http' in spiderLink) or ('www' in spiderLink):
							if urlnohttp in spiderLink:
								existingPages.append(spiderLink.split(urlnohttp, 1)[1])
								print('spider appended: ' + spiderLink.split(urlnohttp, 1)[1])
						elif '/' in spiderLink:
							print('spider appended elif: ' + spiderLink)
							existingPages.append(spiderLink)
						else:
							print('spider appended else: ' + spiderLink)
							existingPages.append('/' + spiderLink)

# Target domain entered as command line argument. Set up authenticate flags.
baseURL = sys.argv[len(sys.argv) - 1]
parser = argparse.ArgumentParser()
parser.add_argument('-u', action='store', dest='username', help='Flag to set username.')
parser.add_argument('-p', action='store', dest='password', help='Flag to set password.')
parser.add_argument('baseURL', action='store', help='Target domain.')

parser_results = parser.parse_args()

username = parser_results.username
password = parser_results.password
automate_login = False

rrr = requests.get(baseURL, allow_redirects=True)
response = rrr.content

if len(rrr.history) >= 2:


	existingPages.append(((rrr.history[len(rrr.history)-1]).url).split(baseURL, 1)[1])

	print('appending 2: '+str((rrr.history[len(rrr.history)-1]).url.split(baseURL, 1)[1]))

	print('append: '+rrr.url.split(baseURL, 1)[1])
	existingPages.append(rrr.url.split(baseURL, 1)[1])


soup = BeautifulSoup(response, "html.parser")
urlnohttp = baseURL.split('://', 1)[1]

# Set authenticate boolean.
print('Target domain: ' + baseURL)
if(username is not None) and (password is not None):
	automate_login = True
	print('Automate Login Active.   Username: ' + username + '    Password: ' + '*' * len(password))
else:
	print('Automate Login Off.')


# Initial spider (unauthenticated).
for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
	if link.has_attr('href'):
		link = link['href']
		# Covers hrefs that are the entire domain.
		if ('http' in link)  or ('www' in link):
			#print('initial appended link: '+link)
			if urlnohttp in link:
				existingPages.append(link.split(urlnohttp, 1)[1])
				print('appended: ' + link.split(urlnohttp, 1)[1])
		# For hrefs that are just the directory.
		elif '/' in link:
			print('initial appended elif: ' + link)
			existingPages.append(link)
		else:
			print('initial appended else: ' + link)
			existingPages.append('/' + link)

spider()

if not automate_login:
	print('Finished unauthenticated spider. Found pages: ' + str(existingPages))
	ProbeWebsite.probeTheWebsite(baseURL, existingPages, None)


if automate_login:
	loginpages = []
	# Do authentication if credentials provided.
	for page in existingPages:
		print('automating: '+page)
		formpassword = ''
		formusername = ''
		founduser = False
		foundpassword = False

		resp = s.get(baseURL + page)
		zzoup = BeautifulSoup(resp.content, "html.parser")
		for form in zzoup.find_all('input'):
			if ('Passw' in str(form)) or ('passw' in str(form)):
				formpassword = form['name']
				# print('Found password field in page: ' + page)
				# print('Form password: ' + form['name'])
				foundpassword = True

			if ('user' in str(form)) or ('email' in str(form)) or ('login' in str(form)):
				formusername = form['name']
				# print('Found username field in page: ' + page)
				# print('Form username: ' + form['name'])
				founduser = True

		if (founduser is True) and (foundpassword is True):
			loginpages.append(page)

			url = baseURL + page
			values = {formpassword: password, formusername: username, 'security_level': 0, 'form': 'submit'}
			temp=s.post(url, data=values)

			print('POSTING: url = '+url)
			print('html user field: '+formusername+'    username: '+username)
			print('html password field: '+formpassword+'    password: '+password)
			#print(temp.content)

	alreadySpidered = []
	spider()

	for page2 in loginpages:
		formpassword2 = ''
		formusername2 = ''
		founduser2 = False
		foundpassword2 = False

		resp = s.get(baseURL + page2)
		zzoup = BeautifulSoup(resp.content, "html.parser")
		for form in zzoup.find_all('input'):
			if ('Passw' in str(form)) or ('passw' in str(form)):
				formpassword2 = form['name']
				# print('Found password field in page: ' + page2)
				# print('Form password: ' + form['name'])
				foundpassword2 = True

			if ('user' in str(form)) or ('email' in str(form)) or 'login' in str(form):
				formusername2 = form['name']
				# print('Found username field in page: ' + page2)
				# print('Form username: ' + form['name'])
				founduser2 = True

		if (founduser2 is True) and (foundpassword2 is True):

			url = baseURL + page2
			values = {formpassword2: password, formusername2: username}
			s.post(url, data=values)

	print('Finished authenticated spider. Found pages: ' + str(existingPages))
	ProbeWebsite.probeTheWebsite(baseURL, existingPages, s)


# Forced Browse
# with open('./files-and-directories.txt') as browselist:
# 	for newline in browselist:
# 		line = newline.rstrip('\n')
# 		# Try a HEAD request to the server with directory from the list.
# 		resp = h.request(baseURL+'/'+line, 'HEAD')
# 		# If the returned status code is not in the 400s or 500s, page exists.
# 		if int(resp[0]['status']) < 400:
# 			existingPages.append(line)
#
# print(existingPages)

