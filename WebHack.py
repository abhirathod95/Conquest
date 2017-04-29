import sys
import httplib2
from bs4 import BeautifulSoup


if len(sys.argv) < 2:
	print('Pass at least a target domain to attack.')
	sys.exit()

baseURL = sys.argv[1]
h = httplib2.Http()
existingPages = []

resp = h.request(baseURL+'/login', 'GET')


with open('./files-and-directories.txt') as browselist:
	for newline in browselist:
		line = newline.rstrip('\n')
		# Try a HEAD request to the server with directory from the list.
		resp = h.request(baseURL+'/'+line, 'HEAD')
		# If the returned status code is not in the 400s or 500s, page exists.
		if int(resp[0]['status']) < 400:
			existingPages.append(line)

print(existingPages)
