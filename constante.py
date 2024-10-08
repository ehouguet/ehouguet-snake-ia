import pygame

class Constante:

  WITH_MUTATION = True
  WITH_LEARNING = False

  NB_ROW = 20
  NB_COLUMN = 30

  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

  TRANSFORMATION = {
    0: [0, -1],
    1: [1, 0],
    2: [0, 1],
    3: [-1, 0]
  }
  OPPOSIT_ACTION = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
  }

  EVENT_EAT_WALL = pygame.USEREVENT + 1 
  EVENT_EAT_VERTEBRATE = pygame.USEREVENT + 2
  EVENT_TOO_MUCH_STEP = pygame.USEREVENT + 3
  EVENT_KILL = pygame.USEREVENT + 4
  EVENT_EAT_APPLE = pygame.USEREVENT + 101 
  