from app.ingest_data import DataIngestor
from app.calculate_metrics import MetricsCalculation



channels, parameters = DataIngestor.ingest_data('./data/channels.txt','./data/parameters.txt')
MetricsCalculation.calculate_metrics(channels,parameters)
