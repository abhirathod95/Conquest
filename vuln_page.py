GET_REQ = 0
POST_REQ = 1

APOSTROPHE = 0
QUOTE = 1

class VulnPage:

	def __init__(self, name, url, vuln, data, req_type, sql):
		self.name = name
		self.url = url
		self.vuln = vuln
		self.data = data
		# 0 FOR GET REQUEST (so data is parameters)
		# 1 FOR POST REQUEST (so data is json)
		self.req_type = req_type
		self.sql = sql

	def __str__(self):
		return "Name: {} URL: {} Vuln: {}".format(self.name, self.url, self.pprint_vuln())

	def __repr__(self):
		return self.name

	def pprint_vuln(self):
		return ",".join(self.vuln)

	def get_data(self):
		return self.data
