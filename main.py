from app.ingest_data import DataIngestor
from app.calculate_metrics import MetricsCalculation
import pandas as pd
import os

#TODO: add an arogument to the execution like --collect-metrics and map that to the metrics collection
# Metrics collection
if os.path.isfile('./data/performance/performance_metrics.csv'):
  metrics = pd.read_csv('./data/performance/performance_metrics.csv')
else:
  metrics = pd.DataFrame()

channels, parameters, metrics = DataIngestor.ingest_data('./data/channels.txt',
                                                './data/parameters.txt',
                                                metrics)
metrics = MetricsCalculation.calculate_metrics(channels,parameters,metrics)

if metrics is not None:
  metrics.to_csv('./data/performance/performance_metrics.csv', index = False)

