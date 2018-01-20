from aggregator import aggregator 
from messenger import messenger 
from config import config
import logging

def main():

	cfg = config.Config()
	ag = aggregator.Aggregator(cfg)
	msgr = messenger.InfluxMessenger(cfg)

	factory_data = ag.aggregate_factory_data()
	
	if type(factory_data) is str:
		msgr.push_failure(factory_data)
	#elif type(factory_data) is None:
	else:
		msgr.push_data(factory_data)

if __name__ == "__main__":
	main()
