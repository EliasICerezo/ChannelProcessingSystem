from app.calculate_metrics import MetricsCalculation
import numpy as np
import pandas as pd
import pytest
import json
import re
import os


class TestCalculateMetrics():
    def setup_method(self):
        clean_files()

    def teardown_class(self):
        clean_files()

    # Tests for calculate_metrics
    def test_calculate_metrics_with_empty_dictionaries_should_return_exception(self):
        with pytest.raises(AttributeError):
            MetricsCalculation.calculate_metrics({}, {})

    def test_calculate_metrics_with_None_performance_metrics_should_return_None_performance_metrics(self):
        _, _, metrics = MetricsCalculation.calculate_metrics({'X': np.array([1])},
                                                             {'c': 0, 'm': 0}, None)
        assert metrics is None

    def test_calculate_metrics_with_not_None_performance_metrics_should_return_more_elements_in_metrics(self):
        metrics = pd.DataFrame()
        start = metrics.shape[0]
        _, _, metrics = MetricsCalculation.calculate_metrics({'X': np.array([1])},
                                                             {'c': 0, 'm': 0}, metrics)
        end = metrics.shape[0]
        assert start < end

    def test_calculate_metrics_with_populated_channels_and_parameters_should_return_more_elements_in_both_channels_and_parameters(self):
        channels = {'X': np.array([1])}
        parameters = {'c': 0, 'm': 0}
        channels_start_keycount = len(channels)
        parameters_start_keycount = len(parameters)

        channels, parameters, _ = MetricsCalculation.calculate_metrics(
            channels, parameters, None)

        channels_end_keycount = len(channels)
        parameters_end_keycount = len(parameters)
        assert channels_start_keycount < channels_end_keycount
        assert parameters_start_keycount < parameters_end_keycount

    def test_calculate_metrics_with_populated_channels_full_of_zeroes_should_raise_a_zero_division_error(self):
        channels = {'X': np.array([0])}
        parameters = {'c': 2, 'm': 2}

        with pytest.raises(ZeroDivisionError):
            _, _, _ = MetricsCalculation.calculate_metrics(
                channels, parameters, None)

    # End to end test for calculate metrics
    def test_calculate_metrics_with_populated_parameters_should_return_correct_calculations(self):
        channels = {'X': np.array([1])}
        parameters = {'c': 0, 'm': 0}
        channels, parameters, _ = MetricsCalculation.calculate_metrics(
            channels, parameters, None)

        assert sum(channels.get('Y')) == 0
        assert sum(channels.get('A')) == 1
        assert sum(channels.get('B')) == 1
        assert sum(channels.get('C')) == 2
        assert parameters.get('b') == 1

    # Tests for can_calculate
    def test_can_calculate_when_called_with_X_channel_None_returns_false(self):
        assert not MetricsCalculation.can_calculate({'X': None}, {})

    def test_can_calculate_when_called_with_m_parameter_None_returns_false(self):
        assert not MetricsCalculation.can_calculate({}, {'m': None})

    def test_can_calculate_when_called_with_c_parameter_None_returns_false(self):
        assert not MetricsCalculation.can_calculate({}, {'c': None})

    def test_can_calculate_when_called_with_X_channel_returns_false(self):
        assert not MetricsCalculation.can_calculate({'X': 0}, {})

    def test_can_calculate_when_called_with_m_parameter_returns_false(self):
        assert not MetricsCalculation.can_calculate({}, {'m': 0})

    def test_can_calculate_when_called_with_c_parameter_returns_false(self):
        assert not MetricsCalculation.can_calculate({}, {'c': 0})

    def test_can_calculate_when_called_with_all_values_populated_as_None_returns_false(self):
        assert not MetricsCalculation.can_calculate({'X': None}, {'c': None,
                                                                             'm': None})

    def test_can_calculate_when_called_with_all_values_populated_but_X_is_not_a_numpy_aray_returns_false(self):
        assert not MetricsCalculation.can_calculate({'X': []}, {'c': 0,
                                                                           'm': 0})

    def test_can_calculate_when_called_with_all_values_populated_but_X_is_an_empty_numpy_aray_returns_false(self):
        assert not MetricsCalculation.can_calculate({'X': np.array([])}, {'c': 0,
                                                                                     'm': 0})

    def test_can_calculate_when_called_with_all_values_populated_but_X_is_an_one_element_numpy_aray_returns_true(self):
        assert MetricsCalculation.can_calculate({'X': np.array([1])}, {'c': 0,
                                                                                  'm': 0})

    def test_can_calculate_when_called_with_all_values_populated_but_X_is_an_n_element_numpy_aray_returns_true(self):
        assert MetricsCalculation.can_calculate({'X': np.array([1, 2, 3, 4])}, {'c': 0,
                                                                                           'm': 0})
    # Tests for can_persist

    def test_can_persist_empty_data_returns_false(self):
        assert not MetricsCalculation.can_persist({})

    def test_can_persist_incorrect_channel_data_returns_false(self):
        assert not MetricsCalculation.can_persist({'X': None})

    def test_can_persist_incorrect_type_channel_data_returns_false(self):
        assert not MetricsCalculation.can_persist({'X': []})

    def test_can_persist_correct_channel_data_returns_true(self):
        assert MetricsCalculation.can_persist({'X': np.array([])})

    def test_can_persist_incorrect_type_parameter_returns_false(self):
        assert not MetricsCalculation.can_persist({'a': None})

    def test_can_persist_int_type_parameter_returns_true(self):
        assert MetricsCalculation.can_persist({'a': 2})

    def test_can_persist_float_type_parameter_returns_true(self):
        assert MetricsCalculation.can_persist({'a': 2.0})

    def test_can_persist_one_channel_empty_data_returns_true(self):
        assert MetricsCalculation.can_persist({'X': np.array([])})

    def test_can_persist_one_channel_full_data_returns_true(self):
        assert MetricsCalculation.can_persist({'X': np.array([1, 2, 3, 4])})

    def test_can_persist_n_channel_empty_data_returns_true(self):
        assert MetricsCalculation.can_persist({'X': np.array([]),
                                               'Y': np.array([])})

    def test_can_persist_n_channel_full_data_returns_true(self):
        assert MetricsCalculation.can_persist({'X': np.array([1, 2, 3, 4]),
                                               'Y': np.array([1.0, 2.0, 3.0, 4.0])})

    # Tests for persist_data
    def test_persist_incorrect_parameters_does_not_create_files(self):
        MetricsCalculation.persist_data({'a': 'incorrect_data'}, 'test')
        regex = re.compile('.*test*')
        directory_contents = os.listdir("./data/processed")
        assert len(list(filter(regex.match, directory_contents))) == 0

    def test_persist_parameters_successfully_creates_files(self):
        MetricsCalculation.persist_data({'a': 0}, 'test')
        regex = re.compile('.*test*')
        directory_contents = os.listdir("./data/processed")
        assert len(list(filter(regex.match, directory_contents))) == 3

    def test_persist_incorrect_channels_does_not_creates_files(self):
        MetricsCalculation.persist_data({'X': 'incorrect_data'}, 'test')
        regex = re.compile('.*test*')
        directory_contents = os.listdir("./data/processed")
        assert len(list(filter(regex.match, directory_contents))) == 0

    def test_persist_channels_successfully_creates_files(self):
        MetricsCalculation.persist_data({'X': np.array([])}, 'test')
        regex = re.compile('.*test*')
        directory_contents = os.listdir("./data/processed")
        assert len(list(filter(regex.match, directory_contents))) == 3

    def test_persist_parameters_contain_something_in_files(self):
        MetricsCalculation.persist_data({'a': 0}, 'test')
        regex = re.compile('.*test*')
        path_to_directory = "./data/processed"
        directory_contents = os.listdir(path_to_directory)
        filtered_contents = list(filter(regex.match, directory_contents))
        for filename in filtered_contents:
            with open(os.path.join(path_to_directory, filename), 'r') as f:
                lines = f.readlines()
                assert len(lines) > 0

    def test_persist_channels_contain_something_in_files(self):
        MetricsCalculation.persist_data({'X': np.array([])}, 'test')
        regex = re.compile('.*test*')
        path_to_directory = "./data/processed"
        directory_contents = os.listdir(path_to_directory)
        filtered_contents = list(filter(regex.match, directory_contents))
        for filename in filtered_contents:
            with open(os.path.join(path_to_directory, filename), 'r') as f:
                lines = f.readlines()
                assert len(lines) > 0

    def test_persist_channels_all_files_contain_same_data(self):
        MetricsCalculation.persist_data({'X': np.array([0])}, 'test')
        regex = re.compile('.*test*')
        path_to_directory = "./data/processed"
        directory_contents = os.listdir(path_to_directory)
        filtered_contents = list(filter(regex.match, directory_contents))

        csv_data, txt_data, json_data = load_files(
            path_to_directory, filtered_contents)
        txt_data = {k: [int(v)] for k, v in txt_data.items()}
        assert txt_data == json_data
        for k in json_data.keys():
            assert json_data[k] == [int(csv_data[k])]
            assert txt_data[k] == [int(csv_data[k])]

    def test_persist_parameters_all_files_contain_same_data(self):
        MetricsCalculation.persist_data({'a': 0}, 'test')
        regex = re.compile('.*test*')
        path_to_directory = "./data/processed"
        directory_contents = os.listdir(path_to_directory)
        filtered_contents = list(filter(regex.match, directory_contents))

        csv_data, txt_data, json_data = load_files(
            path_to_directory, filtered_contents)
        txt_data = {k: int(v) for k, v in txt_data.items()}
        assert txt_data == json_data
        for k in json_data.keys():
            assert json_data[k] == int(csv_data[k])
            assert txt_data[k] == int(csv_data[k])


def clean_files():
    p = re.compile('.*test*')
    path_to_contents = "./data/processed"
    directory_contents = os.listdir(path_to_contents)
    contents_to_delete = list(filter(p.match, directory_contents))
    for c in contents_to_delete:
        os.remove(os.path.join(path_to_contents, c))


def load_files(path_to_directory, filtered_contents):
    for filename in filtered_contents:
        # Since in python the instruction switch case does not exist; ifs must be used
        if filename.endswith('.csv'):
            csv_data = pd.read_csv(os.path.join(path_to_directory, filename))
        elif filename.endswith('.txt'):
            with open(os.path.join(path_to_directory, filename), 'r') as f:
                lines = f.readlines()
                txt_data = {}
                for line in lines:
                    tokens = line.split(',')
                    txt_data[tokens[0]] = tokens[1]
        elif filename.endswith('.json'):
            with open(os.path.join(path_to_directory, filename), 'r') as f:
                json_data = json.load(f)
        else:
            pytest.fail("File extension not recognised")
    return csv_data, txt_data, json_data
