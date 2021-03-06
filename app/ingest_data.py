"""Module that represents the data ingestor for the solution
"""
import time
import os
import numpy as np
import pandas as pd


class DataIngestor():
    """Class ensembling the data ingestor entity
    """
    @staticmethod
    def ingest_data(path_to_channels: str, path_to_parameters: str,
                    metrics: pd.DataFrame = None) -> tuple:
        """Method that loads channels and parameters from file and returns them 
        into adictionary

        Args:
            path_to_channels (str): Path to the channels file
            path_to_parameters (str): Path to parameters file

        Raises:
            Exception: If the parameters or channels are not defined correctly
                       (parameter example: "M ,2.0") (channel example: "x, 0.1, 0.2")
            OSError: If the paths passed as parameter do not reference a file

        Returns:
            tuple : Tuple of 2 elements: Channels and Parameters in that order
        """

        if os.path.isfile(path_to_channels) and os.path.isfile(path_to_parameters):
            # Performance metrics gathering
            if metrics is not None:
                start = time.time()

            channels = {}
            parameters = {}
            with open(path_to_channels) as file:
                lines = file.readlines()
                for line in lines:
                    tokens = line.split(', ')
                    if '' in tokens:
                        tokens.remove('')
                    if len(tokens) < 2:
                        raise Exception(
                            "Error while processing channels: Channel not defined correctly")
                    dataset = [float(e) for e in tokens[1:]]
                    channels[tokens[0]] = np.array(dataset)

            with open(path_to_parameters) as file:
                lines = file.readlines()
                for line in lines:
                    tokens = line.split(', ')
                    if '' in tokens:
                        tokens.remove('')
                    if len(tokens) != 2:
                        raise Exception(
                            "Error while processing parameters: Parameter not defined correctly")
                    parameters[tokens[0]] = float(tokens[1])

            if metrics is not None:
                end = time.time()
                metrics = metrics.append({'key': 'data_loading', 'value': end - start},
                                         ignore_index=True)

            if not DataIngestor.validate_ingested_data(channels, parameters):
                raise Exception(
                    "Channels and parameters are not well defined in the files")

            return channels, parameters, metrics
        else:
            raise OSError(
                "Either of the paths provided do not reference a file")

    @staticmethod
    def validate_ingested_data(channels: dict, parameters: dict) -> bool:
        """Function to validate that the ingested data has the correect casing
        in the names

        Args:
            channels (dict): Imported channels
            parameters (dict): Imported parameters

        Returns:
            bool: Whether the channels and parameters are valid or not
        """
        return all([k.isupper() for k in list(channels.keys())]) and \
            all([k.islower() for k in list(parameters.keys())])
