import sys
import httplib2
import argparse

from bs4 import BeautifulSoup, SoupStrainer

import requests
#import ProbeWebsite

existingPages = []
alreadySpidered = []

s = requests.session()

# Spider method works for our demo website with just 5 lines or so
# but needs loads more code for compatibility with other websites.
def spider():
	while set(existingPages) != set(alreadySpidered):
		for page in existingPages:
			if page not in alreadySpidered:
				resp = s.get(baseURL + page, allow_redirects=False).content
				# print('spidering: '+page)
				alreadySpidered.append(page)
				for spiderLink in BeautifulSoup(resp, "html.parser", parse_only=SoupStrainer('a')):
					if spiderLink.has_attr('href') and (spiderLink['href'] not in existingPages):
						spiderLink = spiderLink['href']
						if 'http' in spiderLink:
							# print('link: ' + spiderLink)
							if urlnohttp in spiderLink:
								existingPages.append(spiderLink.split(urlnohttp, 1)[1])
								# print('appended: ' + spiderLink.split(urlnohttp, 1)[1])
						elif '/' in spiderLink:
							# print('appended elif: ' + spiderLink)
							existingPages.append(spiderLink)

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

h = httplib2.Http()
status, response = h.request(baseURL)
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
		if 'http' in link:
			# print('link: '+link)
			if urlnohttp in link:
				existingPages.append(link.split(urlnohttp, 1)[1])
				# print('appended: ' + link.split(urlnohttp, 1)[1])
		# For hrefs that are just the directory.
		elif '/' in link:
			# print('appended elif: ' + link)
			existingPages.append(link)

# print('initial spider: ' + str(existingPages))
spider()
if not automate_login:
	print('Finished unauthenticated spider. Found pages: ' + str(existingPages))
	#ProbeWebsite.probeTheWebsite(baseURL, existingPages, None)


if automate_login:
	# Do authentication if credentials provided.
	loginPages = []
	for page in existingPages:
		resp = s.get(baseURL + page)
		zzoup = BeautifulSoup(resp.content, "html.parser")
		for form in zzoup.find_all('input'):
			if 'password' in str(form):
				loginPages.append(page)

	print('login pages: ' + str(loginPages))

	for loginpage in loginPages:
		url = baseURL+loginpage
		values = {'Email': username, 'email': username, 'Username':username, 'username': username,
		          'Password': password, 'password': password}
		s.post(url, data=values)

	alreadySpidered = []
	spider()
	print('Finished authenticated spider. Found pages: ' + str(existingPages))
	#ProbeWebsite.probeTheWebsite(baseURL, existingPages, s)


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

