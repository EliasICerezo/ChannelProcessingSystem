# ChannelProcessingSystem
## Data ingestion
In order to feed data into the system, we take as formatting rules the ones applied in the .txt provided as per data so that the system is general enough to accept different variables in the same file whenever they follow the formatting rules of the files provided.
## Persistence of the metrics calculated
Metrics calculated have been stored in both the original format, JSON and CSV. The original format is considered since it is the format that other software in the ecosystem may use per input. JSON is added since it is one of the most popular formats to ingest data into systems as well as is CSV. The latter also can be imported into Excel for data visualization and presentation.
All processed files can be found under `./data/processed/` directory
## Value of the metric 'b'
As per requested in the assignment, the value of the metric 'b' can be found in the channels export. The value obtained in floating point by python (decimal calculation errors may need to be considered) is `6.269852166777007`
# Performance Analysis
After implementing the first solution where only the 4 functions declared in the document were taken in consideration and without any generalization a performance report is generated in order to setup a baseline to see how the performance degrades when generalising the exercise.  
In order to analyse the performance, the execution time of the different parts of the code have been timed, tagged and collected into a CSV to then generate the performance metrics. This collection introduces an overhead and more complexity to the code but any performance analysis does. In the production code this analysis wouldn´t execute but in order for the reader to see the process, the code has been left in the files.
For the analysis to be statistically significative, 30 executions were performed [1].
This performance analysis is merely orientative to demonstrate how the performance degrades when generalising the solution. If we were seeking performance, other language would have been chosen to implement the solution (C or Go for example), but since in the exercise there is no strong indication that performance is key, python has been selected.

## Hardware
The execution of the solution has been performed in a machine with the following system:
![MacBook Pro 16 I9 8 Cores 16GB RAM](images/system.png)

## Metrics data
Data extracted from the metrics can be found under `./data/performance/performance_metrics.csv` in case the reader would like to see the metrics extracted.
A copy of the metrics extracted before the generalization of the solution can also be found in the same folder under the name `./data/performance/performance_metrics_without_generalizing.csv` No improvements in performance were done at the stage of the latter metrics collection, being them the real time consumption from the first solution

## Performance Report

### Metrics of the first solution
<!-- TODO: generate a report with the CSV of the first metrics -->

### Metrics of the generalized solution
<!-- TODO: genrate a report with the CSV of the generalized metrics. Create a code that will generate the statistical report of all the CSVs present in the folder. -->
# References
[1] Hogg, R. V., Tanis, E. A., & Zimmerman, D. L. (1977). Probability and statistical inference (Vol. 993). New York: Macmillan.