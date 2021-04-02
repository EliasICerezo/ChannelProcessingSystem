# ChannelProcessingSystem

## Requirements
* [Python 3](https://www.python.org).  
## Solution structure

* `app` directory: Classes ensembling the behaviour of the system can be found inside this directory.  
* `data` directory: Raw, processed and performance data can be found inside this folder. The main executable writes to `data/processed` and `data/performance`.The raw data needs to be placed under the `data` directory in order to be ingested. In `data/processed` channels and parameter data can be found. In `data/performance` performance metrics data can be found.   
* `test` directory: All unit and E2E tests are presents under this directory.  
* `main.py` file: File that calculates the channels, parameters and gathers the performance metrics. It writes to `data` directory.  
* `performance_report.py` file: It generates the performance report with all the metrics gathered.  

### Execution of the solution
Automated scripts to execute the solution are provided, whether you use Windows, Mac or Linux.
For Windows users execute the .bat file once python 3 is on the path (check by opening a cmd and typing `py --version` and it should return python version installed).
For Mac and Linux users, execute the .sh provided. Linux and Mac usually come with a version of python 3 installed, but chaeck by opening a terminal and running `py --version`.

In order to execute the solution manually follow these steps:
1. Download and install Python.
2. Make sure that python is on the PATH of the system by running `py --version`.
3. Execute `py -m pip install virtualenv`.
4. Execute `py -m venv venv`.
5. If in Windows, run `venv\Scripts\activate`, if in Mac or Linux run `source venv/bin/activate`.
6. Execute `pip install -r requirements.txt`.
7. If you want to run the tests and see the coverage execute `pytest --cov app`.
8. If you want to run the solution, execute `py main.py`.
9. If you want to run the automated performance report generation execute `py performance_report.py`.

### Execution of the tests
## Value of the parameter 'b'
As per requested in the assignment, the value of the parameter 'b' can be found in the parameters export under `data/processed/parameters.csv`. The value obtained in floating point by python (floating point calculation errors may need to be considered) is `6.269852166777007`.
The tests can be run and coverage can be extracted by executing: `pytest --cov app`.
### Test coverage report

| Name                     | Statemets | Miss | Coverage |
|--------------------------|-----------|------|----------|
| app/__init__.py          | 0         | 0    | 100%     |
| app/calculate_metrics.py | 54        | 0    | 100%     |
| app/ingest_data.py       | 41        | 0    | 100%     |
## Data ingestion
In order to feed data into the solution, we take as formatting rules the ones applied in the .txt provided as per data so that the solution is general enough to accept different variables in the same file whenever they follow the formatting rules of the files provided. Note that the original raw files can be found under the `data` directory.  
## Persistence of the metrics calculated
Channels and parameters calculated have been stored in both the original format, JSON and CSV. The original format is the first considered since it is the format that other software in the ecosystem where this solution would be deployed may use per input. JSON is added since it is one of the most popular formats to ingest data into systems as well as CSV is. The latter also can be imported into Excel for data visualization and presentation.  
All processed files can be found under `./data/processed/` directory.  

# Performance Analysis
After implementing the solution, a performance report is generated to provide an idea of the execution time expected.  
In order to analyse the performance, the execution time of the different parts of the code have been timed, tagged and collected into a CSV to then generate the performance report. This collection introduces an overhead and more complexity to the code but any performance analysis does. In the production code this analysis wouldn´t execute but in order for the reader to see the process, the code has been left in the files.  
For the analysis to be statistically significative, 30 executions were performed [1].  
## Hardware
The execution of the solution has been performed in a machine with the following system:
![MacBook Pro 16 I9 8 Cores 16GB RAM](images/system.png)
## Metrics data
Data extracted from the metrics can be found under `./data/performance/performance_metrics.csv` in case the reader would like to see the metrics extracted.

### Performance Report

All values found in the following table are measured in seconds.

| name                | mean                   | std                    | min                   | max                   | confidence.95                                     |
|---------------------|------------------------|------------------------|-----------------------|-----------------------|---------------------------------------------------|
| data_loading        | 0.00038563121448859095 | 0.00018154342285501665 | 0.0003011226654052    | 0.0013601779937744    | [0.0003202606330682824, 0.00045100179590889947] |
| metrics_calculation | 5.226424246123343e-05  | 2.7883069278695677e-06 | 4.887580871582031e-05 | 5.817413330078125e-05 | [5.126022236407643e-05, 5.3268262558390427e-05] |
| metrics_persisting  | 0.005651228355638857   | 0.0013579062083443315  | 0.0044560432434082    | 0.0123078823089599    | [0.005162270303853052, 0.006140186407424662]    |

# Concept of generic.
In the exercise, "flexible and generic" is mentioned. The solution implemented is generic in the sense that the parts are completely decoupled, SOLID principles have been applied in its implementation, any method can be used by other class, the solution is easily extensible and it supports any number of parameters and any number of samples. By adding more samples, the execution time may grow, but thanks to the performance analysis and since in the document nothing is mentioned about efficiency, after the implementation we consider that the system has an acceptable performance. Different output formats are offered bringing flexibility to the data analysis, data presentation and data treatment activities where this solution may reside.  
# Ideas to expand the solution.
In order to generalize the implementation, a solution where the ecuations could be serialised in a file, deserialised, and calculated in order could be implemented.  
This expansion would allow the users to store the equations in a human-readable format (i.e. .txt).  
The .txt would be read and the solution would discover which variables would be missing for each equation.  
If an equation could be calculated, the solution would calculate and append to channels or parameters the results (would depend on the casing).  
The solution would iterate over the different equations and would solve if solvable.  
The solution would be escalable since the worst case scenario would have complexity **O(n*n/2+0.5n)** which is below O(n**2).  
This solution would need extra feedback to understand which are the operations that may need to be supported and how would they be encoded in the serialization.  
This solution would need a lot of extra testing since the use case is broad.  
Without extra feedback on the use case and focusing only in the details provided in the document, this expansion is considered over-engineering and therefore, although some time has been dedicated to put the expansion in perspective and think about it, in the end has not been implemented.  

# References
[1] Hogg, R. V., Tanis, E. A., & Zimmerman, D. L. (1977). Probability and statistical inference (Vol. 993). New York: Macmillan.