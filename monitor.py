import aggregator 
import messenger 
from config import config

def main():
	cfg = config.Config()
	ag = aggregator.Aggregator(cfg)
	msgr = messenger.InfluxMessenger(cfg)

	factory_data = ag.aggregate_factory_data()
	if type(factory_data) is str:
		msgr.push_failure(factory_data)
	elif type(factory_data) is None:
		print "factory_data is empty"
	else:
		msgr.push(factory_data)

if __name__ == "__main__":
	main()
