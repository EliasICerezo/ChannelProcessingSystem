from app.ingest_data import DataIngestor
from app.calculate_metrics import MetricsCalculation
import pandas as pd
import time
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
channels, parameters, metrics = MetricsCalculation.calculate_metrics(channels,parameters,metrics)

# Performance metrics gathering for data persistence
if metrics is not None:
  start = time.time()

MetricsCalculation.persist_data(channels,'channels')
MetricsCalculation.persist_data(parameters,'parameters')

# Performance metrics gathering for data persistence
if metrics is not None:
  end = time.time()
  metrics = metrics.append({'key': 'metrics_persisting', 'value':end-start},
                            ignore_index = True)

if metrics is not None:
  metrics.to_csv('./data/performance/performance_metrics.csv', index = False)

