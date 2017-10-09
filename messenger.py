import httpclient
import os

class Messenger:
	def __init__(self, config):
		self.config = config
		self.httpclient = httpclient.Client(config)
		self.measurement_name = config.get_measurement_name()
		self.current_factory = config.get_current_factory_name()
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.database_name = config.get_database_name()

class InfluxMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)

	def push_failure(self, error_name):
		
		# create database
		self.httpclient.create_database(self.database_name)
		
		line = "Health,errorname=" + error_name + " value=1"

		self.httpclient.post(line)


	def push(self, factory_data):

		# save factory_data to outbox file
		self.save_to_outbox(factory_data)

		# create database
		self.httpclient.create_database(self.database_name)

		# send outbox file to influx
		self.push_outbox()

	def save_to_outbox(self, factory_data):
		# write data to file
		f = open(self.dir_path + '/outbox.txt', 'w')
		
		factory_fragment = "factory=" + self.current_factory

		for entry_name, entry_data in factory_data.items():
			
			entry_fragment = "entryname=" + entry_name
			
			for frontend_name, frontend_data in entry_data.items():
				frontend_fragment = "frontendname=" + frontend_name + " "

				metric_fragment = ""
				for metric_name, metric_data in frontend_data.items():
					metric_fragment += metric_name + "=" + metric_data + ","
				line = self.measurement_name + "," + \
					factory_fragment + "," + \
					entry_fragment + "," + \
					frontend_fragment + " " + \
					metric_fragment[:-1] + \
					"\n"
				f.write(line)
				
		f.close()

	def push_outbox(self):
		f = open(self.dir_path + '/outbox.txt')
		count = 0
		fragment = "\n".join([line for line in f])
		fragment = fragment.replace("\n\n", "\n")
		self.httpclient.post(fragment)



class RabbitMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)
