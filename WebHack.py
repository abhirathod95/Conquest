import sys
import httplib2
import argparse

from bs4 import BeautifulSoup, SoupStrainer



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

if(username is not None) and (password is not None):
	automate_login = True

if automate_login:
	print('Automate Login Active. Username: ' + username + ' Password: ' + password)
else:
	print('Automate Login Off.')

print('Target domain: ' + baseURL)

h = httplib2.Http()
status, response = h.request(baseURL)
soup = BeautifulSoup(response, "html.parser")




# pagesWithInput = []
#
# forms = soup.findAll('form')
# print(forms)
#
# print(len(forms))

# resp = h.request(baseURL+'/login', 'GET')
#
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

# # Begin spidering.
# for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
# 	if link.has_attr('href'):
# 		print(link['href'])


# with open('./files-and-directories.txt') as browselist:
# 	for newline in browselist:
# 		line = newline.rstrip('\n')
# 		# Try a HEAD request to the server with directory from the list.
# 		resp = h.request(target+'/'+line, 'HEAD')
# 		# If the returned status code is not in the 400s or 500s, page exists.
# 		if int(resp[0]['status']) < 400:
# 			pagesWithInput.append(line)

# print(pagesWithInput)
