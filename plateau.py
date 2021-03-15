import random

from constante import Constante


########## class ##########

class Plateau:

  RET_MOVE_EAT_VERTABRATE = 1
  RET_MOVE_EAT_WALL = 2
  RET_MOVE_EAT_APPLE = 3
  RET_MOVE_NORMAL = 4

  def __init__(self, row, column):
    self.nb_row = row
    self.nb_column = column
    self.init()
  
  def init(self):
    # init plateau
    self.grid = [([None for y in range(self.nb_row)]) for x in range(self.nb_column)]
    # init snake
    snakeX = round(self.nb_column / 2)
    snakeY = round(self.nb_row / 2)
    self.snake = Snake(snakeX, snakeY, Constante.DOWN)
    for vertebrate in self.snake.vertebrates:
      self.grid[vertebrate.x][vertebrate.y] = vertebrate
    # init apple
    self.generate_new_apple()
    
  def __str__(self):
    return "<apple: {0} >".format(self.apple.__str__())

  def move(self, direction):
    codeRetour = self.RET_MOVE_NORMAL
    last_first_vertebrate = self.snake.vertebrates[0]
    newCoodinate = self.nextCoordinate(last_first_vertebrate.x, last_first_vertebrate.y, direction)

    # le serpent sort de la zone
    if (self.isOutOfBorder(newCoodinate)):
      return self.RET_MOVE_EAT_WALL
    
    # le serpent se mange la queud
    if (isinstance(self.grid[newCoodinate[0]][newCoodinate[1]], Vertebrate)):
      return self.RET_MOVE_EAT_VERTABRATE

    # gestion du cas ou le serpent mange une pomme
    is_move_on_apple = isinstance(self.grid[newCoodinate[0]][newCoodinate[1]], Apple)
    if is_move_on_apple:
      self.generate_new_apple()
      codeRetour = self.RET_MOVE_EAT_APPLE

    # maj de la premiere vertebre
    last_first_vertebrate.direction = direction
    # supprime la derniere vertebre
    if not is_move_on_apple:
      last_vertebrate = self.snake.vertebrates.pop()
      self.grid[last_vertebrate.x][last_vertebrate.y] = None
    # cree la nouvelle premiere vertebre
    new_first_vertebrate = Vertebrate(newCoodinate[0], newCoodinate[1], -1)
    self.snake.vertebrates = [new_first_vertebrate] + self.snake.vertebrates
    self.grid[new_first_vertebrate.x][new_first_vertebrate.y] = new_first_vertebrate
    return codeRetour

  def generate_new_apple(self):
    appleX = random.randint(0, self.nb_column - 1)
    appleY = random.randint(0, self.nb_row - 1)
    while (self.grid[appleX][appleY] is not None):
      appleX = random.randint(0, self.nb_column - 1)
      appleY = random.randint(0, self.nb_row - 1)
    self.apple = Apple(appleX, appleY)
    self.grid[self.apple.x][self.apple.y] = self.apple

  def isOutOfBorder(self, coordinate):
    if (0 > coordinate[0] 
    or coordinate[0] >= self.nb_column 
    or 0 > coordinate[1] 
    or coordinate[1] >= self.nb_row):
      return True
    return False


  ########## static ##########
  @classmethod
  def lastCoordinate(self, x, y, direction):
    transformation = Constante.TRANSFORMATION[direction]
    return [x - transformation[0], y - transformation[1]]

  @classmethod
  def nextCoordinate(self, x, y, direction):
    transformation = Constante.TRANSFORMATION[direction]
    return [x + transformation[0], y + transformation[1]]

class Apple:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __str__(self):
    return "<x: {0}, y: {1}>".format(self.x, self.y)
    
class Snake:
  def __init__(self, x, y, direction):
    Vertebrate(x, y, direction)
    self.vertebrates = [Vertebrate(x, y, direction)]
    lastCoodinate = Plateau.lastCoordinate(x, y, direction)
    self.vertebrates.append(Vertebrate(lastCoodinate[0], lastCoodinate[1], direction))
    lastCoodinate2 = Plateau.lastCoordinate(lastCoodinate[0], lastCoodinate[1], direction)
    self.vertebrates.append(Vertebrate(lastCoodinate2[0], lastCoodinate2[1], direction))
    
  def __str__(self):
    return "<first_Vertebrate: {0}>".format(self.vertebrates[0])
   
class Vertebrate:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.direction = direction
    
  def __str__(self):
    return "<x: {0}, y: {1}, direction: {2}>".format(self.x, self.y, self.direction)
