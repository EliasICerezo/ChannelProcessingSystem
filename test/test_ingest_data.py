from app.ingest_data import DataIngestor
import pandas as pd
import pytest
import os
import re

class TestIngestData():
  def setup_class(self):
    files_to_create = {
      'empty_test_file.txt':'',
      'invalid_test_channels_file.txt':'x, 2',
      'incorrect_test_channels_file.txt':'X, this_is_a_string',
      'correct_test_channels_file.txt':'X, 1, 2, 3',
      'incomplete_test_channels_file.txt':'X, ',
      'invalid_test_parameters_file.txt':'M, 2',
      'incorrect_test_parameters_file.txt':'m, this_is_a_string',
      'correct_test_parameters_file.txt':'m, 1',
      'incomplete_test_parameters_file.txt':'m, ',
    }
    path_to_directory = './data'
    for k, v in files_to_create.items():
      with open(os.path.join(path_to_directory, k), 'w') as f:
        f.write(v)
  
  def teardown_class(self):
    regex = re.compile('.*test*')
    path_to_dir = './data'
    dir_contents = os.listdir(path_to_dir)
    to_remove = list(filter(regex.match, dir_contents))
    for filename in to_remove:
      os.remove(os.path.join(path_to_dir,filename))

  def test_ingest_data_with_inexistant_paths_returns_exception(self):
    with pytest.raises(OSError):
      DataIngestor.ingest_data('','')

  def test_ingest_data_with_directory_paths_returns_exception(self):
    with pytest.raises(OSError):
      DataIngestor.ingest_data('./data','./data')

  def test_ingest_data_with_both_invalid_files_returns_exception(self):
    with pytest.raises(Exception):
      DataIngestor.ingest_data('./data/invalid_test_channels_file.txt',
                               './data/invalid_test_parameters_file.txt')

  def test_ingest_data_with_one_invalid_files_returns_exception(self):
    with pytest.raises(Exception):
      DataIngestor.ingest_data('./data/invalid_test_channels_file.txt',
                               './data/correct_test_parameters_file.txt')

  def test_ingest_data_with_valid_files_returns_populated_variables(self):
    channels, parameters, _ = DataIngestor.ingest_data(
                                './data/correct_test_channels_file.txt',
                                './data/correct_test_parameters_file.txt')
    assert channels is not None
    assert parameters is not None

  def test_ingest_data_with_None_metrics_returns_None_metrics(self):
    _, _, metrics = DataIngestor.ingest_data(
                      './data/correct_test_channels_file.txt',
                      './data/correct_test_parameters_file.txt',
                      None)
    assert metrics is None

  def test_ingest_data_with_metrics_returns_metrics(self):
    metrics = pd.DataFrame()
    start = len(metrics)
    _, _, metrics = DataIngestor.ingest_data(
                      './data/correct_test_channels_file.txt',
                      './data/correct_test_parameters_file.txt',
                      metrics)
    end = len(metrics)
    assert end > start

  def test_ingest_data_with_one_incorrect_channels_file_returns_exception(self):
    with pytest.raises(ValueError):
      DataIngestor.ingest_data('./data/incorrect_test_channels_file.txt',
                               './data/correct_test_parameters_file.txt')

  def test_ingest_data_with_one_incorrect_parameters_file_returns_exception(self):
    with pytest.raises(ValueError):
      DataIngestor.ingest_data('./data/correct_test_channels_file.txt',
                               './data/incorrect_test_parameters_file.txt')

  def test_ingest_data_with_one_incomplete_channels_file_returns_exception(self):
    with pytest.raises(Exception):
      DataIngestor.ingest_data('./data/incomplete_test_channels_file.txt',
                               './data/correct_test_parameters_file.txt')

  def test_ingest_data_with_one_incomplete_parameters_file_returns_exception(self):
    with pytest.raises(Exception):
      DataIngestor.ingest_data('./data/correct_test_channels_file.txt',
                               './data/incomplete_test_parameters_file.txt')


  
