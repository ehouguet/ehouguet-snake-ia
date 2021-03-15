import random
import math

class Matrix:

  def __init__(self, nb_rows, nb_cols):
    self.nb_rows = nb_rows
    self.nb_cols = nb_cols
    # init matrix
    self.matrix = [([None for y in range(nb_cols)]) for x in range(nb_rows)]
  
  @classmethod
  def SimpleListToMatrix(self, listMatrix):
    if not isinstance(listMatrix, list):
      raise 'listMatrix is not a list'
    newListMatrix = [[None] for y in range(len(listMatrix))]
    for idx in range(len(listMatrix)):
      newListMatrix[idx][0] = listMatrix[idx]
    return Matrix.listToMatrix(newListMatrix)
    
  @classmethod
  def matrixToSimpleList(self, matrix):
    if len(matrix.matrix[0]) != 1:
      raise "listMatrix have not 1 column"
    newListMatrix = [[] for y in range(len(matrix.matrix))]
    for idx in range(len(matrix.matrix)):
      newListMatrix[idx] = matrix.matrix[idx][0]
    return newListMatrix
    
  @classmethod
  def listToMatrix(self, listMatrix):
    if not isinstance(listMatrix, list):
      raise 'listMatrix is not a list'
    if len(listMatrix) < 0:
      raise 'listMatrix is empty'
    matrix = Matrix(len(listMatrix), len(listMatrix[0]))
    matrix.matrix = listMatrix
    return matrix
    
  @classmethod
  def matrixToList(self, matrix):
    return matrix.matrix

  # sigmoid la function d'activation
  @classmethod
  def sigmoid(self, x):
    y = 1 / (1 + pow(math.e, -x))
    #y = (x + 1) / 2
    #print('sigmoid({}) = {}'.format(x, y))
    return y

  # logit la function desactivation
  @classmethod
  def logit(self, y):
    x = y * 2 - 1
    #print('logit({}) = {}'.format(y, x))
    return x

  # clone
  def clone(self):
    clone = Matrix(self.nb_rows, self.nb_cols)
    for idxR in range(self.nb_rows):
      for idxC in range(self.nb_cols):
        clone.matrix[idxR][idxC] = self.matrix[idxR][idxC]
    return clone
    
  # multipli cette matris et celle en parametre
  def multiply(self, matrix2):
    if (self.nb_cols != matrix2.nb_rows):
      raise 'invalid multiplication'
    result = Matrix(self.nb_rows, matrix2.nb_cols)
    for idxR in range(result.nb_rows):
      for idxC in range(result.nb_cols):
        sum = 0.0
        for idxCommun in range(matrix2.nb_rows):
          sum += self.matrix[idxR][idxCommun] * matrix2.matrix[idxCommun][idxC]
        result.matrix[idxR][idxC] = sum
    return result
    
  # aditionne cette matris et celle en parametre
  def addition(self, matrix2):
    if (self.nb_cols != matrix2.nb_cols 
      or self.nb_rows != matrix2.nb_rows):
      raise 'invalid addition'
    result = Matrix(self.nb_rows, self.nb_cols)
    for idxR in range(result.nb_rows):
      for idxC in range(result.nb_cols):
        result.matrix[idxR][idxC] = self.matrix[idxR][idxC] + matrix2.matrix[idxR][idxC]
    return result
    
  # soustrait cette matris et celle en parametre
  def subtract(self, matrix2):
    if (self.nb_cols != matrix2.nb_cols 
      or self.nb_rows != matrix2.nb_rows):
      raise 'invalid subtraction'
    result = Matrix(self.nb_rows, self.nb_cols)
    for idxR in range(result.nb_rows):
      for idxC in range(result.nb_cols):
        result.matrix[idxR][idxC] = self.matrix[idxR][idxC] + matrix2.matrix[idxR][idxC]
    return result
    
  # multipli cette matris et celle en parametre
  def rotate90(self):
    result = Matrix(self.nb_cols, self.nb_rows)
    for idxR in range(result.nb_rows):
      for idxC in range(result.nb_cols):
        result.matrix[idxR][idxC] = self.matrix[idxC][idxR]
    return result

  # recupere la valeur
  def activate(self):
    Matrix_result = Matrix(self.nb_rows, self.nb_cols)
    for idxR in range(self.nb_rows):
      for idxC in range(self.nb_cols):
        Matrix_result.matrix[idxR][idxC] = Matrix.sigmoid(self.matrix[idxR][idxC])
    return Matrix_result
    
  # recupere la valeur
  def desactivate(self):
    Matrix_result = Matrix(self.nb_rows, self.nb_cols)
    for idxR in range(self.nb_rows):
      for idxC in range(self.nb_cols):
        Matrix_result.matrix[idxR][idxC] = Matrix.logit(self.matrix[idxR][idxC])
    return Matrix_result
    
  def mutate(self, intensity):
    newMatrix = self.clone()
    row_to_mutate = random.randint(0, self.nb_rows - 1)
    col_to_mutate = random.randint(0, self.nb_cols - 1)
    actual_value = newMatrix.matrix[row_to_mutate][col_to_mutate]
    len_range_value_mutation = 2 * intensity
    start_range_value_mutation = max(-1, min(1, actual_value - len_range_value_mutation / 2))
    value_to_mutate = random.random() * len_range_value_mutation + start_range_value_mutation
    value_to_mutate = max(-1, min(1, value_to_mutate))
    newMatrix.matrix[row_to_mutate][col_to_mutate] = value_to_mutate
    return newMatrix
    
  def learn(self, inputs, output, output_want):
    if (len(output) != len(output_want)):
      raise 'output is incompatible'
    matrix_output = Matrix.listToMatrix([output])
    matrix_output_want = Matrix.listToMatrix([output_want])
    matrix_delta = matrix_output.subtract(matrix_output_want)
    matrix_delta = matrix_delta.rotate90()
    matrix_delta_desactivate = matrix_delta.desactivate()
    matrix_inputs = Matrix.listToMatrix([inputs])
    matrix_modification = matrix_delta_desactivate.multiply(matrix_inputs)
    return self.addition(matrix_modification)
