try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

BASE_DIR = "/var/lib/gwms-factory/web-area/monitor/"
SCHEDD_STATUS_FILE = "schedd_status.xml"

# TODO abstract xml parsing from aggregator
class Aggregator:
	def __init__(self, config):
		self.config = config

	def aggregate_factory_data(self):
		filename = BASE_DIR + SCHEDD_STATUS_FILE
		metrics = self.config.get_metrics()
		factory_data = dict()
	
		# Event based iteration
        	xml_iterator = iter(ET.iterparse(filename, events=("start", "end")))

		# go through all entries
        	for event, elem in xml_iterator:
			# save data for each entry we encounter...
                	if event == 'start' and elem.tag == 'entry':
				entry_name = elem.get("name")
				entry_data = dict()
			
				# go through all frontends
				for event, elem in xml_iterator:

					# save data for each frontend we encounter...
					if event == 'start' and elem.tag == 'frontend':
						frontend_name = elem.get("name") # TODO error handle
						frontend_data = dict()
					
						# fast forward document index until we get to the Status of the frontend
						while elem.tag != 'Status':
							elem.clear()
							event, elem = xml_iterator.next()

						for metric in metrics:
							frontend_data[metric] = elem.get(metric) # TODO error handle

						entry_data[frontend_name] = frontend_data
						elem.clear()

					# ...until we reach the end of all frontends for this entry
					elif event == 'end' and elem.tag == 'frontends':
						factory_data[entry_name] = entry_data 
						elem.clear()
						break
					else:
						elem.clear()
				
			# ...until we reach the end of all entries for this factory
			elif event == 'end' and elem.tag == 'entries':
				elem.clear()
				return factory_data
			else:
                		elem.clear()

