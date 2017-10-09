try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

BASE_DIR = "/var/lib/gwms-factory/web-area/monitor/"
SCHEDD_STATUS_FILE = "schedd_status.xml"
SCHEDD_ATTRIB_FILE = "rrd_Status_Attributes.xml"

# TODO abstract xml parsing from aggregator
class Aggregator:
	def __init__(self, config):
		self.config = config

	def aggregate_factory_data(self):
		schedd_status_data = self.aggregate_schedd_status()
		if type(schedd_status_data) is not dict:
			print "error coming from Aggregator.aggregate_schedd_status"
		schedd_attrib_data = self.aggregate_schedd_attributes()
		if type(schedd_attrib_data) is not dict:
			print "error coming from Aggregator.aggregate_schedd_attributes"
		
		factory_data = merge_dicts([schedd_status_data, schedd_attrib_data])
		
		return factory_data

	def aggregate_schedd_status(self):
		filename = BASE_DIR + SCHEDD_STATUS_FILE
		factory_data = dict()
	
		# Event based iteration
        	xml_iterator = iter(ET.iterparse(filename, events=("start", "end")))

		# go through all entries
        	for event, elem in xml_iterator:
			# save data for each entry we encounter...
                	if event == 'start' and elem.tag == 'entry':
				entry_name = elem.get("name")
				if entry_name is None:
					print "Malformed XML: an entry does not have a name attribute"
					return "malformed_xml"
				entry_data = dict()
			
				# go through all frontends
				for event, elem in xml_iterator:

					# save data for each frontend we encounter...
					if event == 'start' and elem.tag == 'frontend':
						frontend_name = elem.get("name") 
						if frontend_name is None:
							print "Malformed XML: frontend in entry %s does not have a name attribute" % entry_name
							return "malformed_xml"
						frontend_data = dict()
					
						# fast forward document index until we get to the Status of the frontend
						while elem.tag != 'Status':
							# handle case where we never find Status (ie. malformed xml document)
							if event == 'end' and elem.tag == 'frontend':
								print "Malformed XML: frontend %s does not have a Status element" % frontend_name
								return "malformed_xml"
							else:
								elem.clear()
								event, elem = xml_iterator.next()

						for metric in self.config.get_schedd_status_metrics():
							frontend_data[metric] = elem.get(metric)
							if frontend_data[metric] is None:
								print "Metric %s does not exist for entry %s frontend %s" % (metric, entry_name, frontend_name)
								return "metric_does_not_exist"

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

	def aggregate_schedd_attributes(self):
		filename = BASE_DIR + SCHEDD_ATTRIB_FILE
		factory_data = dict()
	
		# Event based iteration
        	xml_iterator = iter(ET.iterparse(filename, events=("start", "end")))

		# go through all entries
        	for event, elem in xml_iterator:
			# save data for each entry we encounter...
                	if event == 'start' and elem.tag == 'entry':
				entry_name = elem.get("name")
				if entry_name is None:
					print "Malformed XML: an entry does not have a name attribute"
					return "malformed_xml"
				entry_data = dict()
			
				# go through all frontends
				for event, elem in xml_iterator:

					# save data for each frontend we encounter...
					if event == 'start' and elem.tag == 'frontend':
						frontend_name = elem.get("name") 
						if frontend_name is None:
							print "Malformed XML: frontend in entry %s does not have a name attribute" % entry_name
							return "malformed_xml"
						else:
							ls = frontend_name.split('_')
							if ls[0] == 'frontend':
								frontend_name = "_".join(ls[1:])
							
						frontend_data = dict()
					
						# fast forward document index until we get to the period of the frontend
						while elem.get("name") != '7200':
							# handle case where we never find period (ie. malformed xml document)
							if event == 'end' and elem.tag == 'frontend':
								print "Malformed XML: frontend %s does not have a period element with a name attribute \"7200\"" % frontend_name
								return "malformed_xml"
							else:
								elem.clear()
								event, elem = xml_iterator.next()

						for metric in self.config.get_schedd_attrib_metrics():
							frontend_data[metric] = elem.get(metric)
							if frontend_data[metric] is None:
								print "Metric %s does not exist for entry %s frontend %s" % (metric, entry_name, frontend_name)
								return "metric_does_not_exist"

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

