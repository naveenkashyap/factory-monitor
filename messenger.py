import httpclient

class Messenger:
	def __init__(self, config):
		self.config = config
		self.httpclient = httpclient.Client(config)
		self.measurement_name = config.get_measurement_name()
		self.current_factory = config.get_current_factory_name()

class InfluxMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)

	def push(self, factory_data):

		self.save_to_outbox(factory_data)
		# create database
		self.httpclient.create_database()

		# write data file to measurement

	def save_to_outbox(self, factory_data):
		# write data to file
		f = open('outbox.txt', 'w')
		
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



class RabbitMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)
