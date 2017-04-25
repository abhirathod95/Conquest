import sys
from subprocess import call
from bs4 import BeautifulSoup


if len(sys.argv) < 2:
	print('Pass at least a target domain to attack.')
	sys.exit()

# Takes a domain to run a nikto scan on; output is a .txt file. Script will wait until subprocess completes
call('nikto -o test.txt -h ' + sys.argv[1], shell=True)

with open('test.txt') as nikto_output:
	for line in nikto_output:
		continue
# gonna wait to see what the site looks like before parsing
