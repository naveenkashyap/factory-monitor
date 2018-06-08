#!/usr/bin/python
from aggregator import aggregator 
from messenger import messenger 
from config import config
import logging

def main():

	cfg = config.Config()

	logging.basicConfig(filename=cfg.get_logfile_loc(), format='%(asctime)s %(message)s', level=logging.DEBUG)

	ag = aggregator.Aggregator(cfg)
	msgr = messenger.InfluxMessenger(cfg)

	log_debug("aggregating factory data")
	factory_data = ag.aggregate_factory_data()
	
	if factory_data is None:
		log_debug("factory data aggregation FAILED")
		return

	log_debug("factory data aggregation SUCCEEDED")
	msgr.push_data(factory_data)

def log_debug(msg):
	logging.debug("DEBUG: monitor.py: %s" % msg)

if __name__ == "__main__":
	main()
