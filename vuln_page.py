GET_REQ = 0
POST_REQ = 1

class VulnPage:

	def __init__(self, name, url, vuln, data, req_type):
		self.name = name
		self.url = url
		self.vuln = vuln
		# THIS IS FOR POST REQUEST VULNERABILITIES
		self.data = data
		# 0 FOR GET REQUEST (so data is parameters)
		# 1 FOR POST REQUEST (so data is json)
		self.req_type = req_type

	def __str__(self):
		return "Name: {} URL: {} Vuln: {}".format(self.name, self.url, self.pprint_vuln())

	def __repr__(self):
		return self.name

	def pprint_vuln(self):
		return ",".join(self.vuln)

	def get_data(self):
		return self.data
