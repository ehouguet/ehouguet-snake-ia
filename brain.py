import random
import pygame

from constante import Constante
from neuralNet import NeuralNet
from plateau import Plateau, Vertebrate

# une matrice par etapes

# trois lignes pour les trois inputs de sorti respectivement:
#  - gauche
#  - en face
#  - droite

# les colones signifis respectivement :
#  - distance du mur a gauche
#  - distance du mur en face
#  - distance du mur a droite
#  - distance de la vertebre a gauche
#  - distance de la vertebre en face
#  - distance de la vertebre a droite
#  - pomme a gauche
#  - pomme en face
#  - pomme a droite
basiqueWeights = [
  [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
  ],
  [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
  ]
]

# une version inteligente
workWeights = [
  [
    [0.2, 0.1, 0, -0.4, -0.9, -0.4, 0.3, 0.0, -0.1],
    [0.1, -0.1, 0.6, 0.8, 0.2, -0.6, 0.0, 0.0, 0.0],
    [0.0, 0.7, 0.0, -0.1, -0.2, -0.5, 0.3, -0.6, -0.1], 
    [-0.5, -0.9, 0.1, -0.7, 0.1, -0.9, -0.2, 0.7, -0.3], 
    [0.3, -0.1, 0.0, 0.0, -0.4, -0.0, 0.1, 0.0, 0.1],
    [1, -0.4, -0.0, 0.1, 0.3, -0.0, 0.3, -0.2, -0.0]
  ],
  [
    [1.0, 0.0, 0.5, -0.1, -0.9, 0.0],
    [0.7, 0.3, -0.24, -0.4, 0.4, -0.8],
    [0.0, 0.0, 0.9, -0.3, -0.6, 0.1]
  ]
]

# une version stack
workStack = [
  [
    [-0.10313540802392107, 0.0, -0.17868380570345227, 0.2878482232616439, 0.0, 0.4749457482914541, 0.0, 0.24061473657324883, 0.0],
    [-0.26694879354783063, 0.1033003992288265, 0.0, -0.798934100874128, 0.30028212303357327, 0.03563698344874383, -0.4013734773047454, 0.10882173897871839, 0.00692322242502047],
    [0.19747902358689362, -0.17839762359930927, 0.0, 0.046645575079956536, 0.0, 0.1890068979514209, -0.10810083237493329, 0.8599028806073662, -0.11279393771974121],
    [0.0, 0.47400001268862435, 0.0, -0.0521139016795, 0.3579144733744245, -0.6078565511703642, 0.7958011217385723, -0.16460174724982948, 0.0],
    [-0.4702714032442429, 0.0, 0.9511571679198376, 0.0, 0.695694281443384, -0.09166909541710262, -0.10831235261070615, -0.18871555692073982, -0.16948091464370074],
    [0.05118135814357416, 0.5674232297419222, 0.2645616057237967, 0.5951191225570409, -0.1710712569210565, 0.0, 0.0, -0.1856124199101089, 0.0]
  ],
  [
    [0.40251010522437164, 0.18782831954734885, 0.099224078534806, 0.12169633896703218, 0.37980479028404823, -0.10887478986199259],
    [-0.03101612466205872, -0.15402608267538098, 0.327497216046561, 0.13952331732638817, -0.18557595103438662, -0.05796770530236289],
    [0.061050361234612494, 0.9184017206580601, -0.17988468728036822, 0.960083146973935, -0.9163652573076659, 0.4495460255004589]
  ]
]

class Brain:

  def __init__(self):
    self.betterNeuralNetWeights = NeuralNet.createWithList(basiqueWeights)
    self.betterScore = 0
    self.generation = 1
    self.nb_mutation = 2
    self.mutation_intensity = 1
    self.currentNeuralNetWeights = self.betterNeuralNetWeights
    self.last_inputs = None
    self.last_outputs = None
  
  def reacted(self, game):
    #print(" ----------------- ")
    neuralInputs = self.extract_neural_inputs(game)
    #print("neuralInputs : {}".format(neuralInputs))
    neuralOutput = self.currentNeuralNetWeights.getOutput(neuralInputs)
    #print("neuralOutput : {}".format(neuralOutput))
    inputs_choise = self.choise_key_input(game, neuralOutput)
    #print("inputs_choise : {}".format(inputs_choise))
    self.last_inputs = neuralInputs
    self.last_outputs = neuralOutput
    event = pygame.event.Event(pygame.KEYDOWN, key=inputs_choise)
    pygame.event.post(event)

  def extract_neural_inputs(self, game):
    neuralInputs = [None for y in range(len(basiqueWeights[0][0]))]
    last_direction = game.last_direction
    left_direction = ((last_direction - 1) % 4)
    right_direction = ((last_direction + 1) % 4)
    # distance du mur a gauche
    neuralInputs[0] = self.getNeuralInputHaveAWall(left_direction, game)
    # distance du mur en face
    neuralInputs[1] = self.getNeuralInputHaveAWall(last_direction, game)
    # distance du mur a droite
    neuralInputs[2] = self.getNeuralInputHaveAWall(right_direction, game)
    # distance d'une vertabre a gauche
    neuralInputs[3] = self.getNeuralInputHaveAVertabrate(left_direction, game)
    # distance d'une vertabre en face
    neuralInputs[4] = self.getNeuralInputHaveAVertabrate(last_direction, game)
    # distance d'une vertabre a droite
    neuralInputs[5] = self.getNeuralInputHaveAVertabrate(right_direction, game)
    # pome a gauche
    neuralInputs[6] = self.getNeuralInputApplePosition(left_direction, game)
    # pome en face
    neuralInputs[7] = self.getNeuralInputApplePosition(last_direction, game)
    # pome a droite
    neuralInputs[8] = self.getNeuralInputApplePosition(right_direction, game)
    # biais des noeuds
    #neuralInputs[9] = 1
    return neuralInputs

  def getNeuralInputApplePosition(self, direction, game):
    last_vertabrate = game.plateau.snake.vertebrates[0]
    apple = game.plateau.apple
    if direction == Constante.UP:
      if apple.y < last_vertabrate.y:
        return 1
      else:
        return 0
    if direction == Constante.DOWN:
      if apple.y > last_vertabrate.y:
        return 1
      else:
        return 0
    if direction == Constante.RIGHT:
      if apple.x > last_vertabrate.x:
        return 1
      else:
        return 0
    if direction == Constante.LEFT:
      if apple.x < last_vertabrate.x:
        return 1
      else:
        return 0

  def getNeuralInputHaveObstacle(self, direction, game):
    last_vertabrate = game.plateau.snake.vertebrates[0]
    obstacleToCome = self.getCoordinateToObstacleToCome(direction, [last_vertabrate.x, last_vertabrate.y], game)
    distance = abs(last_vertabrate.x - obstacleToCome[0] + last_vertabrate.y - obstacleToCome[1])
    if (distance == 2):
      return 0.2
    if (distance == 1):
      return 1
    return 0
    
  def getNeuralInputHaveAWall(self, direction, game):
    last_vertabrate = game.plateau.snake.vertebrates[0]
    obstacleToCome = self.getCoordinateToObstacleToCome(direction, [last_vertabrate.x, last_vertabrate.y], game)
    if (not game.plateau.isOutOfBorder(obstacleToCome)):
      return 0
    distance = abs(last_vertabrate.x - obstacleToCome[0] + last_vertabrate.y - obstacleToCome[1])
    if (distance == 2):
      return 0.2
    if (distance == 1):
      return 1
    return 0

  def getNeuralInputHaveAVertabrate(self, direction, game):
    last_vertabrate = game.plateau.snake.vertebrates[0]
    obstacleToCome = self.getCoordinateToObstacleToCome(direction, [last_vertabrate.x, last_vertabrate.y], game)
    if (
      game.plateau.isOutOfBorder(obstacleToCome) 
      or not isinstance(game.plateau.grid[obstacleToCome[0]][obstacleToCome[1]], Vertebrate)):
      return 0
    distance = abs(last_vertabrate.x - obstacleToCome[0] + last_vertabrate.y - obstacleToCome[1])
    if (distance == 2):
      return 0.2
    if (distance == 1):
      return 1
    return 0

  def getNeuralInputDistanceObstacle(self, direction, game):
    last_vertabrate = game.plateau.snake.vertebrates[0]
    obstacleToCome = self.getCoordinateToObstacleToCome(direction, [last_vertabrate.x, last_vertabrate.y], game)
    distance = abs(last_vertabrate.x - obstacleToCome[0] + last_vertabrate.y - obstacleToCome[1])
    return distance / (max(Constante.NB_ROW, Constante.NB_COLUMN) + 1)

  def getCoordinateToObstacleToCome(self, direction, last_coordinate, game):
    next_coordinate = Plateau.nextCoordinate(last_coordinate[0], last_coordinate[1], direction)
    # le serpent sort de la zone
    if (0 > next_coordinate[0] 
    or next_coordinate[0] >= Constante.NB_COLUMN 
    or 0 > next_coordinate[1] 
    or next_coordinate[1] >= Constante.NB_ROW):
      return next_coordinate
    # le serpent se mange la queud
    if (isinstance(game.plateau.grid[next_coordinate[0]][next_coordinate[1]], Vertebrate)):
      return next_coordinate
    return self.getCoordinateToObstacleToCome(direction, next_coordinate, game)

  def choise_key_input(self, game, ouput):
    snackeNewOriantation = self.choise_good_output(game, ouput) - 1
    inputs = [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]
    last_direction = game.last_direction
    return inputs[(snackeNewOriantation + last_direction) % 4]
    
  def choise_good_output(self, game, ouput):
    output_choise = 1
    if (ouput[1] < ouput[0] and ouput[2] < ouput[0]):
      output_choise = 0
    if (ouput[1] < ouput[2] and ouput[0] < ouput[2]):
      output_choise = 2
    return output_choise
    
  def learn(self, event, game):
    print(" ----------------- ")
    ouput_choise = self.choise_good_output(game, self.last_outputs)
    output_want = [output for output in self.last_outputs]
    if (event == Constante.EVENT_EAT_APPLE):
      output_want[ouput_choise] = 1
    if (event == Constante.EVENT_EAT_WALL
      or event == Constante.EVENT_EAT_VERTEBRATE):
      output_want[ouput_choise] = 0
      
    print('self.last_inputs : {}'.format(self.last_inputs))
    print('self.last_outputs : {}'.format(self.last_outputs))
    print('output_want : {}'.format(output_want))
    self.betterNeuralNetWeights.learn(self.last_inputs, self.last_outputs, output_want)
    print('new NeuralNets : {}'.format(self.betterNeuralNetWeights.matrixInOut.matrix))

  def nextGeneration(self, game):
    score = game.score
    print('matrix score : {}'.format(score))
    print('last better score : {}'.format(self.betterScore))
    if (score > self.betterScore):
      print('next generation : {}'.format(self.generation))
      self.betterNeuralNetWeights = self.currentNeuralNetWeights
      self.betterScore = game.score
      self.generation += 1
    else:
      self.betterScore = max(0, self.betterScore - max(0.05, 0.2 / self.generation))
    # faire mutater les poids
    self.mutation_intensity = max(0.2, 1 - self.betterScore / (Constante.NB_ROW + 20))
    self.currentNeuralNetWeights = self.betterNeuralNetWeights
    for idx_mutation in range(0, self.nb_mutation):
      self.currentNeuralNetWeights = self.currentNeuralNetWeights.mutate(self.mutation_intensity)
    print(' ------------------- ')
    print('matrix use : {}'.format(self.currentNeuralNetWeights.toList()))


  def increase_nb_mutation(self):
    self.nb_mutation = self.nb_mutation + 1
  def decrease_nb_mutation(self):
    self.nb_mutation = self.nb_mutation - 1