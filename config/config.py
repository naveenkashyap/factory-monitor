import os
import json

FILE = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

class Config:
	def __init__(self):
		with open(FILE) as config_file:
			self.data = json.load(config_file)

	def get_schedd_status_location(self):
		return self.data['schedd_status_location']
	
	def get_client_metrics(self):
		return self.data['client_metrics']

	def get_requested_metrics(self):
		return self.data['requested_metrics']

	def get_status_metrics(self):
		return self.data['status_metrics']
	
	def get_database_url(self):
		return self.data['database_URL']
	
	def get_database_username(self):
		return self.data['username']

	def get_database_password(self):
		return self.data['password']
	
	def get_database_name(self):
		return self.data['database_name']

	def get_measurement_name(self):
		return self.data['measurement_name']

	def get_current_factory_name(self):
		return self.data['factory_name']
