class VulnPage:

	def __init__(self, name, url, vuln, data):
		self.name = name
		self.url = url
		self.vuln = vuln
		self.data = data

	def __str__(self):
		return "Name: {} URL: {} Vuln: {}".format(self.name, self.url, self.pprint_vuln())

	def __repr__(self):
		return self.name

	def pprint_vuln(self):
		return ",".join(self.vuln)
