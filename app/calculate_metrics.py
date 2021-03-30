class MetricsCalculation():

  @staticmethod
  def calculate_metrics(channels:dict, parameters:dict):
    Y = [(parameters.get('m')*x+parameters.get('c')) for x in channels.get('X')]
    A = [1/x for x in channels.get('X')]
    if len(A) != len(Y):
      raise Exception('The 2 channels required to calculate B do not have the same number of elements')
    B = [A[i] + Y[i] for i in range(len(Y))]
    b = sum(B) / len(B)
    C = [x+b for x in channels.get('X')]
    
    breakpoint()

  # TODO: Create a way of persisting the metrics as per function 

  