import logging
import os
from http import httpclient

class Messenger:
	def __init__(self, config):
		self.config = config
		self.httpclient = httpclient.Client(config)

		self.measurement_name = config.get_measurement_name()
		if self.measurement_name is None:
			log_error("configuration file not set")

		self.database_name = config.get_database_name()
		if self.database_name is None:
			log_error("configuration file not set")

		self.current_factory = config.get_current_factory_name()
		if self.current_factory is None:
			log_error("configuration file not set")

		self.dir_path = os.path.dirname(os.path.realpath(__file__))

class InfluxMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)

	def push_data(self, factory_data):

		# save factory_data to outbox file
		log_debug("saving factory data to outbox")
		self.save_to_outbox(factory_data)

		# create database
		self.httpclient.create_database(self.database_name)

		# send outbox file to influx
		log_debug("pushing factory data to database")
		self.push_outbox()

	def save_to_outbox(self, factory_data):
		try:
			# write data to file
			f = None
			f = open(self.dir_path + '/outbox/outbox.txt', 'w')
		
			factory_fragment = "factory=" + self.current_factory

			for entry_name, entry_data in factory_data.items():
			
				entry_fragment = "entryname=" + entry_name
				
				for frontend_name, frontend_data in entry_data.items():
					frontend_fragment = "frontendname=" + frontend_name + " "
	
					metric_fragment = ""
					for metric_name, metric_data in frontend_data.items():
						metric_fragment += str(metric_name) + "=" + str(metric_data) + ","
					line = self.measurement_name + "," + \
						factory_fragment + "," + \
						entry_fragment + "," + \
						frontend_fragment + " " + \
						metric_fragment[:-1] + \
						"\n"
					f.write(line)
		except IOError as e:
			log_error(str(e))					
		finally:
			if f is not None:
				f.close()

	def push_outbox(self):
		try:
			f = None
			f = open(self.dir_path + '/outbox/outbox.txt')
			fragment = "\n".join([line for line in f])
			fragment = fragment.replace("\n\n", "\n")
			self.httpclient.post(fragment)
		except IOError as e:
			log_error(str(e))
		finally:
			if f is not None:
				f.close()

class RabbitMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)

def log_debug(msg):
	logging.debug("DEBUG: messenger.py: %s" % msg)

def log_error(msg):
	logging.error("ERROR: messenger.py: %s" % msg)

