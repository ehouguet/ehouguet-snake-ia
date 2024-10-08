from matrix import Matrix

class NeuralNet:

  # contructeur
  def __init__(self, matrixs):
    self.nb_input = matrixs[0].nb_rows
    self.nb_output = matrixs[len(matrixs) - 1].nb_cols
    self.matrixs = matrixs
  
  @classmethod
  def createWithList(self, listesMatrixs):
    matrixs = [[None] for y in range(len(listesMatrixs))]
    for idx in range(len(listesMatrixs)):
      matrixs[idx] = Matrix.listToMatrix(listesMatrixs[idx])
    return NeuralNet.createWithMatrix(matrixs)

  @classmethod
  def createWithMatrix(self, matrixs):
    return NeuralNet(matrixs)

  # methode
  def getOutput(self, listInput):
    if (len(listInput) != self.matrixs[0].nb_cols):
      raise "la longeur de l'input ne corespond pas"
    inputOutput = Matrix.SimpleListToMatrix(listInput)
    for idx in range(len(self.matrixs)):
      inputOutput = self.matrixs[idx].multiply(inputOutput)
    matrixOutputActivate = inputOutput.activate()
    return Matrix.matrixToSimpleList(matrixOutputActivate)

  def mutate(self, intensity):
    matrixsMutate = [[None] for y in range(len(self.matrixs))]
    for idx in range(len(self.matrixs)):
      matrixsMutate[idx] = self.matrixs[idx].mutate(intensity)
    return NeuralNet.createWithMatrix(matrixsMutate)
  
  def learn(self, inputs, output, output_want):
    new_matrix = self.matrixInOut.learn(inputs, output, output_want)
    self.matrixInOut = new_matrix

  def toList(self):
    listesMatrix = [[None] for y in range(len(self.matrixs))]
    for idx in range(len(self.matrixs)):
      listesMatrix[idx] = Matrix.matrixToList(self.matrixs[idx])
    return listesMatrix