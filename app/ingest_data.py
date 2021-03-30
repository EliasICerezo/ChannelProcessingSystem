import os

class DataIngestor():
  """Class ensembling the data ingestor entity
  """
  @staticmethod
  def ingest_data(path_to_channels:str, path_to_parameters:str) -> tuple:
    """Function that processes channels and parameters and returns them into a
    dictionary

    Args:
        path_to_channels (str): Path to the channels file
        path_to_parameters (str): Path to parameters file

    Raises:
        Exception: If the parameters or channels are not defined correctly
                   (parameter example: "m ,2.0") (channel example: "x, 0.1, 0.2")
        OSError: If the paths passed as parameter do not reference a file

    Returns:
        tuple : Tuple of 2 elements: Channels and Parameters in that order 
    """
    if os.path.isfile(path_to_channels) and os.path.isfile(path_to_parameters):
      channels = {}
      parameters = {}
      with open(path_to_channels) as f:
        lines = f.readlines()
        for line in lines:
          tokens = line.split(',')
          if len(tokens) < 2:
            raise Exception("Error while processing channels: Channel not defined correctly")
          channels[tokens[0]] = [float(e) for e in tokens[1:]]
      
      with open(path_to_parameters) as f:
        lines = f.readlines()
        for line in lines:
          tokens = line.split(',')
          if len(tokens) != 2:
            raise Exception("Error while processing parameters: Parameter not defined correctly")
          parameters[tokens[0]] = float(tokens[1])
      
      return channels,parameters
    else:
      raise OSError("Either of the paths provided do not reference a file")