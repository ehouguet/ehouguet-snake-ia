import pygame

from plateau import Plateau
from constante import Constante

########## class ##########

class Game:

  @classmethod
  def emitEvent(self, name):
    event = pygame.event.Event(name)
    pygame.event.post(event)

  def __init__(self, row=10, column=10):
    self.plateau = Plateau(row, column)
    self.last_direction = Constante.DOWN
    self.score = 0
    self.nb_step = 0
    self.nb_step_max_by_score = (row + column) * 2 + 10
    
  def init(self):
    self.last_direction = Constante.DOWN
    self.score = 0
    self.nb_step = 0
    self.plateau.init()
    
  def move(self, direction):
    if Constante.OPPOSIT_ACTION[self.last_direction] == direction:
      return False
    self.last_direction = direction
    coderetour = self.plateau.move(direction)
    if (coderetour == Plateau.RET_MOVE_NORMAL):
      self.nb_step += 1
      if (self.nb_step > (self.nb_step_max_by_score * (self.score + 1))):
        self.emitEvent(Constante.EVENT_TOO_MUCH_STEP)
    if (coderetour == Plateau.RET_MOVE_EAT_WALL):
      self.emitEvent(Constante.EVENT_EAT_WALL)
    if (coderetour == Plateau.RET_MOVE_EAT_VERTABRATE):
      self.emitEvent(Constante.EVENT_EAT_VERTEBRATE)
    if (coderetour == Plateau.RET_MOVE_EAT_APPLE):
      self.score += 1
      self.emitEvent(Constante.EVENT_EAT_APPLE)
    return coderetour

  ########## action des buttons ##########
  def increase_nb_step(self):
    self.nb_step_max_by_score = self.nb_step_max_by_score - 1

  def decrease_nb_step(self):
    self.nb_step_max_by_score = self.nb_step_max_by_score + 1
    
  def kill(self):
    self.emitEvent(Constante.EVENT_KILL)

