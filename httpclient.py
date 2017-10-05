import urllib
import urllib2

class Client:
	def __init__(self, config):
		self.config = config
		self.database_url = config.get_database_url()
		self.database_name = config.get_database_name()
		self.database_password = config.get_database_password()
		self.database_username = config.get_database_username()

	def create_database(self):
		query = "CREATE DATABASE " + self.database_name
		url = self.database_url + "/query?"
		values = {'q': query,
			  'u': self.database_username,
			  'p': self.database_password }
		url += urllib.urlencode(values)
		req = urllib2.Request(url)
		resp = urllib2.urlopen(req)
		print resp
		# TODO error handle

	def post(self, data):
		url = self.database_url + "/write?"
		values = {'db': self.database_name,
			  'precision': 's',
			  'u': self.database_username,
			  'p': self.database_password }
		url += urllib.urlencode(values)
		req = urllib2.Request(url, data)
		resp = urllib2.urlopen(req)
		print resp
		# TODO error handle
		
