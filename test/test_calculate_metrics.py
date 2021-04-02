from app.calculate_metrics import MetricsCalculation
import numpy as np
import pandas as pd
import pytest
import re
import os

class TestCalculateMetrics():
  def setup_method(self):
    p = re.compile('test*')
    path_to_contents = "./data/processed"
    directory_contents = os.listdir(path_to_contents)
    contents_to_delete = list(filter(p.match, directory_contents))
    for c in contents_to_delete:
      os.remove(os.path.join(path_to_contents,c))

  # Tests for calculate_metrics
  def test_calculate_metrics_with_empty_dictionaries_should_return_exception(self):
    with pytest.raises(AttributeError):
      MetricsCalculation.calculate_metrics({},{})

  def test_calculate_metrics_with_None_performance_metrics_should_return_None_performance_metrics(self):
    _, _, metrics = MetricsCalculation.calculate_metrics({'X':np.array([1])},
                                                        {'c':0,'m':0}, None) 
    assert metrics is None

  def test_calculate_metrics_with_not_None_performance_metrics_should_return_more_elements_in_metrics(self):
    metrics = pd.DataFrame()
    start = metrics.shape[0]
    _, _, metrics = MetricsCalculation.calculate_metrics({'X':np.array([1])},
                                                        {'c':0,'m':0}, metrics)
    end = metrics.shape[0]
    assert start < end

  def test_calculate_metrics_with_populated_channels_and_parameters_should_return_more_elements_in_both_channels_and_parameters(self):
    channels = {'X':np.array([1])}
    parameters = {'c':0,'m':0}
    channels_start_keycount = len(channels)
    parameters_start_keycount = len(parameters)
    
    channels, parameters, _ = MetricsCalculation.calculate_metrics(channels, parameters, None)

    channels_end_keycount = len(channels)
    parameters_end_keycount = len(parameters)
    assert channels_start_keycount < channels_end_keycount
    assert parameters_start_keycount < parameters_end_keycount

  def test_calculate_metrics_with_populated_channels_full_of_zeroes_should_raise_a_zero_division_error(self):
    channels = {'X':np.array([0])}
    parameters = {'c':2,'m':2}
    
    with pytest.raises(ZeroDivisionError):
      _, _, _ = MetricsCalculation.calculate_metrics(channels, parameters, None)

  #End to end test for calculate metrics
  def test_calculate_metrics_with_populated_parameters_should_return_correct_calculations(self):
    channels = {'X':np.array([1])}
    parameters = {'c':0,'m':0}
    channels, parameters, _ = MetricsCalculation.calculate_metrics(channels, parameters, None)

    assert sum(channels.get('Y')) == 0
    assert sum(channels.get('A')) == 1
    assert sum(channels.get('B')) == 1
    assert sum(channels.get('C')) == 2
    assert parameters.get('b') == 1

  # Tests for is_possible_to_calculate
  def test_is_possible_to_calculate_when_called_with_X_channel_None_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({'X':None},{})

  def test_is_possible_to_calculate_when_called_with_m_parameter_None_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({},{'m':None})

  def test_is_possible_to_calculate_when_called_with_c_parameter_None_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({},{'c':None})

  def test_is_possible_to_calculate_when_called_with_X_channel_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({'X':0},{})

  def test_is_possible_to_calculate_when_called_with_m_parameter_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({},{'m':0})

  def test_is_possible_to_calculate_when_called_with_c_parameter_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({},{'c':0})

  def test_is_possible_to_calculate_when_called_with_all_values_populated_as_None_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({'X':None},{'c':None,
                                                              'm':None})
                                                            
  def test_is_possible_to_calculate_when_called_with_all_values_populated_but_X_is_not_a_numpy_aray_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({'X':[]},{'c':0,
                                                              'm':0})

  def test_is_possible_to_calculate_when_called_with_all_values_populated_but_X_is_an_empty_numpy_aray_returns_false(self):
    assert not MetricsCalculation.is_possible_to_calculate({'X':np.array([])},{'c':0,
                                                              'm':0})

  def test_is_possible_to_calculate_when_called_with_all_values_populated_but_X_is_an_one_element_numpy_aray_returns_true(self):
      assert MetricsCalculation.is_possible_to_calculate({'X':np.array([1])},{'c':0,
                                                              'm':0})

  def test_is_possible_to_calculate_when_called_with_all_values_populated_but_X_is_an_n_element_numpy_aray_returns_true(self):
      assert MetricsCalculation.is_possible_to_calculate({'X':np.array([1,2,3,4])},{'c':0,
                                                              'm':0})
# Tests for persist_data

# TEST THAT CREATES THE FILES
# TEST THAT THE FILES GET CREATED EMPTY
# TEST THAT THE FILES CONTAIN SOMETHING WHEN INPUTTING SOMETHING
# TEST THAT ALL 3 FILES HAVE THE SAME CONTENT IN DIFFERENT FORMATS
