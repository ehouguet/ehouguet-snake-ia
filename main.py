from time import sleep
import pygame

from game import Game
from window import Window
from brain import Brain
from constante import Constante

class Main:
  def __init__(self):
    self.window = Window(Constante.NB_ROW, Constante.NB_COLUMN)
    self.game = Game(Constante.NB_ROW, Constante.NB_COLUMN)

    self.brain = Brain()

    self.speed_manual = False
    self.speed = 0.02

  def main(self):

    continuer = True
    while continuer:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          continuer = False
        # joue et reflechie
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP or event.key == pygame.K_z:
            self.game.move(Constante.UP)
          elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.game.move(Constante.DOWN)
          elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
            self.game.move(Constante.LEFT)
          elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.game.move(Constante.RIGHT)
        elif (event.type == Constante.EVENT_EAT_APPLE):
          if (Constante.WITH_LEARNING):
            self.brain.learn(event.type, self.game)
        elif (event.type == Constante.EVENT_EAT_WALL 
        or event.type == Constante.EVENT_EAT_VERTEBRATE
        or event.type == Constante.EVENT_TOO_MUCH_STEP
        or event.type == Constante.EVENT_KILL):
          print("game over")
          if (Constante.WITH_MUTATION):
            self.brain.nextGeneration(self.game)
          if (Constante.WITH_LEARNING):
            self.brain.learn(event.type, self.game)
          self.game.init()
      # affiche
      self.window.display(self, self.game, self.brain)
      # choisi un coup
      self.brain.reacted(self.game)
      # maj speed
      if (self.speed_manual == False):
        if (self.game.score > self.brain.betterScore):
          self.speed = 0.02
        else:
          self.speed = max(0.0000005, self.speed * 0.99)

      sleep(self.speed)
    
  def lunch_better(self):
    self.speed = 0.02
    self.speed_manual = True
    self.brain.currentNeuralNetWeights = self.brain.betterNeuralNetWeights
    self.game.init()
    
  def increase_speed(self):
    self.speed_manual = True
    self.speed = max(0.00000005, self.speed - 0.0001)
    
  def decrease_speed(self):
    self.speed_manual = True
    self.speed = min(0.02, self.speed + 0.0001)

  def speed_auto(self):
    self.speed_manual = False

if __name__ == '__main__':
  main = Main()
  main.main()