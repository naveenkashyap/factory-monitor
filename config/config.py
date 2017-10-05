import os
import json

dirpath = os.path.dirname(os.path.realpath(__file__))
FILE = dirpath + '/config.json'

class Config:
	def __init__(self):
		with open(FILE) as config_file:
			self.data = json.load(config_file)

	def get_metrics(self):
		return self.data['metrics']
	
	def get_database_url(self):
		return self.data['databaseURL']
	
	def get_database_username(self):
		return self.data['username']

	def get_database_password(self):
		return self.data['password']
	
	def get_database_name(self):
		return self.data['databaseName']

	def get_measurement_name(self):
		return self.data['measurementName']

	def get_current_factory_name(self):
		return os.environ['HOSTNAME'].split('.')[0]
