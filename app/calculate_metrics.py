"""Class that calculate the metrics as the exercise requests
"""
import json
import time
import pandas as pd
import numpy as np
class MetricsCalculation():
  """Class that ensembles the metrics calculator.
  """
  @staticmethod
  def calculate_metrics(channels:dict, parameters:dict,
                        metrics:pd.DataFrame = None) -> tuple:
    """Function that calculates the metrics using the different functions provided
    in the system specification

    Args:
        channels (dict): Dictionary containing the channels that have been loaded
        previously.
        parameters (dict): Dictionary containing the parameters that have been loaded
        before
        metrics (pd.DataFrame, optional): Dataframe containing the performance
        metrics. Defaults to None.

    Raises:
        Exception: If the channels required to calculate B do not have the same
        number of elements

    Returns:
        tuple: Tuple containing the calculated channels, calculated parameters
        and metrics
    """
    if not MetricsCalculation.can_calculate(channels,parameters):
      raise AttributeError("Parameters and channels required for metrics \
                           processing are not present")
    # Performance metrics gathering
    if metrics is not None:
      start = time.time()
    channels['Y'] = (parameters.get('m')*channels.get('X')+parameters.get('c'))
    if sum(channels['X']) == 0:
      raise ZeroDivisionError("Dividing by zero")
    channels['A'] = 1/channels.get('X')
    channels['B'] = channels.get('A') + channels.get('Y')
    parameters['b'] = np.mean(channels.get('B'))
    channels['C'] = channels.get('X') + parameters['b']

    # Performance metrics gathering
    if metrics is not None:
      end = time.time()
      metrics = metrics.append({'key': 'metrics_calculation', 'value':end-start},
                               ignore_index = True)

    return channels, parameters, metrics

  @staticmethod
  def can_calculate(channels:dict, parameters:dict) -> bool:
    """Method that validates the inputs for the metrics processing

    Args:
        channels (dict): Data channels
        parameters (dict): Parameters data

    Returns:
        bool: Whether the processing can be performed or not
    """
    if 'X' not in channels or 'm' not in parameters or 'c' not in parameters or \
      channels.get('X') is None or parameters.get('m') is None or \
      parameters.get('c') is None or not isinstance(channels.get('X'),np.ndarray) or \
      len(channels.get('X')) == 0:
      return False
    else:
      return True


  @staticmethod
  def can_persist(data:dict) -> bool:
    """Method that evaluates whether the results can be persisted
    It discovers if the data to be stored is Channel or Parameter data and
    checks the data types contained inside the data object.

    Args:
        data (dict): Data to be stored

    Returns:
        bool: Whether the data can be or not persisted
    """
    if len(data) == 0:
      return False
    if all( [k.isupper() for k in [*data]] ):
      return all([isinstance(v, np.ndarray) for v in list(data.values())])
    else:
      return all([ isinstance(v,(int,float)) for v in list(data.values())])

  @staticmethod
  def persist_data(data:dict, name:str):
    """Function that persists the data in CSV, JSON and the original format

    Args:
        data (dict): Dictionary containing the data to be stored
        name (str): Name of the file to be ammended (the full name of the file
                    will include "processed_NAME" where NAME is the content
                    of this variable)
    """
    # Early return
    if not MetricsCalculation.can_persist(data):
      return

    if [*data][0].isupper():
      data = {k: v.tolist() for k,v in data.items()}
    # Writes to JSON
    with open('./data/processed/processed_{}.json'.format(name),'w') as file:
      file.write(json.dumps(data, indent=4))
    # Writes to the original format
    with open('./data/processed/processed_{}.txt'.format(name),'w') as file:
      for k,v in data.items():
        try:
          line = "{}, {}\n".format(k,", ".join(map(str,v)))
        except:
          line = "{}, {}\n".format(k,str(v))
        file.write(line)
    # Writes to CSV
    try:
      data_df = pd.DataFrame(data)
    except:
      data_df = pd.DataFrame(data, index=[0])
    data_df.to_csv('./data/processed/processed_{}.csv'.format(name), index=False)
