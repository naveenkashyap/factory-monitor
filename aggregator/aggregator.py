import json
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

SCHEDD_STATUS_FILE = "schedd_status.xml"
COMPLETED_DATA_FILE = "completed_data.json"

# TODO abstract xml parsing from aggregator
class Aggregator:
	def __init__(self, config):
		self.config = config
		self.monitor_dir = config.get_monitor_dir()

	def aggregate_factory_data(self):
		schedd_filename = self.monitor_dir + SCHEDD_STATUS_FILE
		completed_filename = self.monitor_dir + COMPLETED_DATA_FILE
		schedd_status_data = self.aggregate_schedd_data(schedd_filename)
		completed_data = self.aggregate_completed_data(completed_filename)
		# TODO error handle

		merged_dicts = merge_dicts([schedd_status_data, completed_data])

		return merged_dicts

	def aggregate_completed_data(self, filename):
		factory_data = dict()
		try:
			completed_data_fp = open(filename)
		except IOError as e:
			print str(e)
			return -1
    
		completed_data = json.load(completed_data_fp)
		entries = completed_data['stats']['entries']
		for entry_name in entries:
			entry_data = dict()
			frontends = entries[entry_name]['frontends']
			for frontend_name in frontends:
				frontend_data = dict()
				for metric, value in frontends[frontend_name]['completed']['stats'].items():
					frontend_data['completed_' + metric] = value
				for metric, value in frontends[frontend_name]['completed_stats']['stats'].items():
					frontend_data['completed_stats_' + metric] = value
				for metric, value in frontends[frontend_name]['completed_wastetime']['stats'].items():
					frontend_data['completed_wastetime_' + metric] = value
				entry_data[frontend_name] = frontend_data
			factory_data[entry_name] = entry_data
		return factory_data

	def aggregate_schedd_data(self, filename):
		factory_data = dict()
	
		# Event based iteration
        	xml_iterator = iter(ET.iterparse(filename, events=("start", "end")))

		# go through all entries
        	for event, elem in xml_iterator:
			# save data for each entry we encounter...
                	if event == 'start' and elem.tag == 'entry':
				entry_data = dict()
				entry_name = elem.get("name")
				if entry_name is None:
					print "Malformed XML: an entry does not have a name attribute"
					return "malformed_xml"
			# skip totals for each entry
			elif event == 'start' and elem.tag == 'total':
				while(event != 'end' or elem.tag != 'total'):
					event, elem = xml_iterator.next()
			
			# save data for each frontend we encounter...
			elif event == 'start' and elem.tag == 'frontend':
				frontend_data = dict()
				frontend_name = elem.get("name") 
				if frontend_name is None:
					print "Malformed XML: frontend in entry %s does not have a name attribute" % entry_name
					return "malformed_xml"

			elif event == 'start' and elem.tag == 'ClientMonitor':
					#for metric in self.config.get_client_metrics():
					for metric, value in elem.items():
						frontend_data["client_" + metric] = value
			elif event == 'start' and elem.tag == 'Requested':
					#for metric in self.config.get_requested_metrics():
					for metric, value in elem.items():
						frontend_data["requested_" + metric] = value
			elif event == 'start' and elem.tag == 'Status':
					#for metric in self.config.get_status_metrics():
					for metric, value in elem.items():
						frontend_data["status_" + metric] = value
	
			elif event == 'end' and elem.tag == 'frontend':
				entry_data[frontend_name] = frontend_data
				elem.clear()

			# ...until we reach the end of all frontends for this entry
			elif event == 'end' and elem.tag == 'frontends':
				factory_data[entry_name] = entry_data
				elem.clear()

			# ...until we reach the end of all entries for this factory
			elif event == 'end' and elem.tag == 'entries':
				elem.clear()
				return factory_data
			else:
                		elem.clear()

def merge_dicts(dicts):
	if len(dicts) <= 1:
		return dicts

	master_dict = dict()

	for d in dicts:
		for entry_name, entry_data in d.items():
			for frontend_name, frontend_data in entry_data.items():
				try:
					master_dict[entry_name][frontend_name].update(frontend_data)
				except KeyError:
					try:
						master_dict[entry_name][frontend_name] = frontend_data
					except KeyError:
						master_dict[entry_name] = dict()
						master_dict[entry_name][frontend_name] = frontend_data
							
	return master_dict

