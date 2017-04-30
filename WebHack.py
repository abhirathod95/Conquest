import sys
import httplib2
import argparse

from bs4 import BeautifulSoup, SoupStrainer

import requests

existingPages = []
alreadySpidered = []

existingPagesAuth = []
alreadySpideredAuth = []

s = requests.session()

def spider():
	while set(existingPages) != set(alreadySpidered):
		for page in existingPages:
			if page not in alreadySpidered:
				resp = s.get(baseURL + page).content
				alreadySpidered.append(page)
				# print('spidering: ' + page)
				for link in BeautifulSoup(resp, "html.parser", parse_only=SoupStrainer('a')):
					if link.has_attr('href') and link['href'] not in existingPages:
						existingPages.append(link['href'])

# Target domain entered as command line argument.
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

print('Target domain: ' + baseURL)
if(username is not None) and (password is not None):
	automate_login = True
	print('Automate Login Active.   Username: ' + username + '    Password: ' + '*' * len(password))
else:
	print('Automate Login Off.')


# Initial spider (unauthenticated).
for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
	if link.has_attr('href'):
		existingPages.append(link['href'])

spider()
print('Finished unauthenticated spider. Found pages: ' + str(existingPages))


#############################################################################

if automate_login:
	# # Do authentication if credentials provided.
	# loginPages = ['', 'login', 'login.php', 'signin', 'signin.php']
	# for loginPage in loginPages:
	# 	print('Iterating login pages: ' + loginPage)
	# 	resp = h.request(baseURL + '/' + loginPage, 'GET')
	# 	if int(resp[0]['status']) < 400:
	# 		print('found')
	# 	else:
	# 		print('not found')

	url = 'http://localhost:5000/login'
	values = {'email': '1', 'password': '1'}

	s.post(url, data=values)
	print('cookie: '+ str(s.cookies.get_dict()))

	existingPagesAuth = existingPages[:]
	alreadySpideredAuth = alreadySpidered[:]
	existingPages = []
	alreadySpidered = []

	# Initial spider (authenticated).
	for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
		if link.has_attr('href'):
			existingPages.append(link['href'])
	spider()
	print('Finished authenticated spider. Found pages: ' + str(existingPages))


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

