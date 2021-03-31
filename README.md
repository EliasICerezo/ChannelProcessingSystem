# ChannelProcessingSystem
## Data ingestion
In order to feed data into the system, we take as formatting rules the ones applied in the .txt provided as per data so that the system is general enough to accept different variables in the same file whenever they follow the formatting rules of the files provided.
## Persistence of the metrics calculated
Metrics calculated have been stored in both the original format, JSON and CSV. The original format is considered since it is the format that other software in the ecosystem may use per input. JSON is added since it is one of the most popular formats to ingest data into systems as well as is CSV. The latter also can be imported into Excel for data visualization and presentation.
All processed files can be found under `./data/processed/` directory
# Value of the metric 'b'
As per requested in the assignment, the value of the metric 'b' can be found in the channels export. The value obtained in floating point by python (decimal calculation errors may need to be considered) is `6.269852166777007`