import aggregator 
import messenger 
from config import config

def main():
	cfg = config.Config()
	ag = aggregator.Aggregator(cfg)
	msgr = messenger.InfluxMessenger(cfg)

	factory_data = ag.aggregate_factory_data()
	msgr.push(factory_data)

if __name__ == "__main__":
	main()
