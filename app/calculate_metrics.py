import json
import time
import pandas as pd
class MetricsCalculation():

  @staticmethod
  def calculate_metrics(channels:dict, parameters:dict,
                        metrics:pd.DataFrame = None):
    
    # Performance metrics gathering
    if metrics is not None:
      start = time.time()
    
    channels['Y'] = [(parameters.get('m')*x+parameters.get('c')) for x in channels.get('X')]
    channels['A'] = [1/x for x in channels.get('X')]
    if len(channels['A']) != len(channels['Y']):
      raise Exception('The 2 channels required to calculate B do not have the same number of elements')
    channels['B'] = [channels['A'][i] + channels['Y'][i] for i in range(len(channels['Y']))]
    parameters['b'] = sum(channels['B']) / len(channels['B'])
    channels['C'] = [x+parameters['b'] for x in channels.get('X')]
    
    # Performance metrics gathering
    if metrics is not None:
      end = time.time()
      metrics = metrics.append({'key': 'metrics_calculation', 'value':end-start},
                               ignore_index = True)

    # Performance metrics gathering
    if metrics is not None:
      start = time.time()
    
    MetricsCalculation.persist_data(channels, 'channels')
    MetricsCalculation.persist_data(parameters, 'parameters')
    
    # Performance metrics gathering
    if metrics is not None:
      end = time.time()
      metrics = metrics.append({'key': 'metrics_persisting', 'value':end-start},
                               ignore_index = True)
    
    return metrics

  @staticmethod
  def persist_data(data:dict, name:str, metrics: pd.DataFrame = None):
    """Function that persists the data in CSV, JSON and the original format

    Args:
        data (dict): Dictionary containing the data to be stored
        name (str): Name of the file to be ammended (the full name of the file 
                    will include "processed_NAME" where NAME is the content 
                    of this variable)
    """     
    # Writes to JSON
    with open('./data/processed/processed_{}.json'.format(name),'w') as f:
      f.write(json.dumps(data, indent=4))
    # Writes to the original format
    with open('./data/processed/processed_{}.txt'.format(name),'w') as f:
      for k,v in data.items():
        try:
          line = "{}, {}\n".format(k,", ".join(map(str,v)))
        except:
          line = "{}, {}\n".format(k,str(v))
        f.write(line)
    # Writes to CSV
    try:
      data_df = pd.DataFrame(data)
    except:
      data_df = pd.DataFrame(data, index=[0])
    data_df.to_csv('./data/processed/processed_{}.csv'.format(name), index=False)
    
  