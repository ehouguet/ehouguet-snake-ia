from matrix import Matrix

class NeuralNet:

  # contructeur
  def __init__(self, nb_input, nb_output):
    self.nb_input = nb_input
    self.nb_output = nb_output

    self.matrixInOut = Matrix(nb_output + 1, nb_input)
  
  @classmethod
  def createWithMatrix(self, matrix):
    neuralNet = NeuralNet(matrix.nb_rows, matrix.nb_cols)
    neuralNet.matrixInOut = matrix
    return neuralNet

  @classmethod
  def createWithList(self, listMatrix):
    matrix = Matrix.listToMatrix(listMatrix)
    return NeuralNet.createWithMatrix(matrix)
  
  # methode
  def getOutput(self, listInput):
    if (len(listInput) != self.matrixInOut.nb_cols):
      raise "la longeur de l'input ne corespond pas"
    matrixInput = Matrix.SimpleListToMatrix(listInput)
    matrixOutput = self.matrixInOut.multiply(matrixInput)
    matrixOutputActivate = matrixOutput.activate()
    return Matrix.matrixToSimpleList(matrixOutputActivate)

  def mutate(self, intensity):
    return NeuralNet.createWithMatrix(self.matrixInOut.mutate(intensity))
  
  def learn(self, inputs, output, output_want):
    new_matrix = self.matrixInOut.learn(inputs, output, output_want)
    self.matrixInOut = new_matrix
