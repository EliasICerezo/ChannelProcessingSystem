from numpy.ma import flatten_structured_array
import pandas as pd
import numpy as np
import scipy.stats
import os
import re


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * data
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


if __name__ == "__main__":
    path_to_dir = './data/performance'
    performance_csvs = os.listdir(path_to_dir)
    regex = re.compile('.*.csv')
    filtered_csvs = list(filter(regex.match, performance_csvs))
    for csv_path in filtered_csvs:
        df = pd.read_csv(os.path.join(path_to_dir, csv_path))
        metrics_names = list(df['key'].unique())
        performance_report = pd.DataFrame(columns=['name', 'mean', 'std', 'min',
                                                   'max', 'confidence.95'])
        for metric in metrics_names:
            is_metric = df['key'] == metric
            metric_data = df[is_metric]
            metric_array = np.array(metric_data['value'].tolist())
            _, low_limit, high_limit = confidence_interval = mean_confidence_interval(
                metric_array)
            row = {'name': metric,
                   'mean': metric_array.mean(),
                   'std': metric_array.std(),
                   'min': metric_array.min(),
                   'max': metric_array.max(),
                   'confidence.95': [low_limit, high_limit], }
            performance_report = performance_report.append(
                row, ignore_index=True)

        performance_report.to_csv(os.path.join(path_to_dir,
                                               "report_{}".format(csv_path)),
                                  index=False)
