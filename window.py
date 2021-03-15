import pygame
from displayGraph import DisplayGraph
from constante import Constante

pygame.init()

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

FONT_SIZE = 16
FONT_WIDTH = 10

PURPLE = (67,51,142)
YELLOW = (246,211,48)

class Window:

  def __init__(self, nb_row, nb_col):
    self.block_size = min(WINDOW_WIDTH / nb_col, WINDOW_HEIGHT / nb_row)
    self.plateau_start_x = WINDOW_WIDTH / 2 - self.block_size * nb_col / 2
    self.plateau_start_y = WINDOW_HEIGHT / 2 - self.block_size * nb_row / 2
    # defini la taile de la fenetre
    self.window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    # defini le titre de la fenetre
    pygame.display.set_caption('Snakoma')
    
    # Renderer for snake and apple
    self.snake = pygame.Surface([self.block_size, self.block_size])
    self.snake.fill(PURPLE)
    self.apple = pygame.Surface([self.block_size, self.block_size])
    self.apple.fill(YELLOW)

    # affiche le fond de jeu blanc
    self.white_box = pygame.Surface([nb_col * self.block_size, nb_row * self.block_size])
    self.white_box.fill((255, 255, 255))
    
    # affiche le fond de fenetre noir
    self.black_box = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
    self.black_box.fill((200, 200, 200))
            
    # cree la font pour le test des generations
    self.font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

    # cree de l'afficheur de graph
    self.displayGraph = DisplayGraph(
      self.window, 
      WINDOW_WIDTH / 2, 
      0, 
      WINDOW_WIDTH / 2, 
      WINDOW_WIDTH / 4,
      [
        'WG', 'WF', 'WD',
        'VG', 'VF', 'VD',
        'AG', 'AF', 'AD'
      ], 
      [
        'GAUCHE',
        'FACE',
        'DROITE'
      ])
    

  def display(self, main, game, brain):
    #print(game.plateau)
    
    # renders fond noir
    self.window.blit(self.black_box, [0,0])

    # renders fond blanc
    self.window.blit(self.white_box, [self.plateau_start_x,self.plateau_start_y])

    # Renders snake
    for vertebrate in game.plateau.snake.vertebrates:
      pos_x = self.plateau_start_x + vertebrate.x * self.block_size
      pos_y = self.plateau_start_y + vertebrate.y * self.block_size
      self.window.blit(self.snake, (pos_x, pos_y))

    # Renders apple
    pos_x = self.plateau_start_x + game.plateau.apple.x * self.block_size
    pos_y = self.plateau_start_y + game.plateau.apple.y * self.block_size
    self.window.blit(self.apple, (pos_x, pos_y))

    # affiche la generation
    self.draw_text('G{}'.format(brain.generation), FONT_WIDTH * 3, FONT_SIZE * 0.5)
    # affiche le dernier mellieur score
    self.draw_text('S{}'.format(round(brain.betterScore, 1)), FONT_WIDTH * 3, FONT_SIZE * 1.5)
    # affiche le nombre max de coup autorise
    self.draw_text('C{}'.format(game.nb_step_max_by_score), FONT_WIDTH * 3, FONT_SIZE * 2.5)
    self.button('-', FONT_WIDTH * 7.5, FONT_SIZE * 2.5, game.increase_nb_step)
    self.button('+', FONT_WIDTH * 8.5, FONT_SIZE * 2.5, game.decrease_nb_step)
    
    # affiche le boutton de kill du serpent en court
    self.button('kill', FONT_WIDTH * 8, FONT_SIZE * 0.5, game.kill, True)
    # affiche le boutton de lancement du meilleur modele
    if (Constante.WITH_MUTATION):
      self.button('better', FONT_WIDTH * 8, FONT_SIZE * 1.5, main.lunch_better)
    
    # affiche la rapiditer d'affichage
    self.draw_text('S{}'.format(round(main.speed, 6)), FONT_WIDTH * 3, FONT_SIZE * 3.5)
    self.button('-', FONT_WIDTH * 7.5, FONT_SIZE * 3.5, main.decrease_speed)
    self.button('+', FONT_WIDTH * 8.5, FONT_SIZE * 3.5, main.increase_speed)
    self.button('auto', FONT_WIDTH * 12.5, FONT_SIZE * 3.5, main.speed_auto)
    
    # affiche le nombre de mutation
    if (Constante.WITH_MUTATION):
      self.draw_text('M{}'.format(brain.nb_mutation), FONT_WIDTH * 3, FONT_SIZE * 4.5)
      self.button('-', FONT_WIDTH * 7.5, FONT_SIZE * 4.5, brain.decrease_nb_mutation, True)
      self.button('+', FONT_WIDTH * 8.5, FONT_SIZE * 4.5, brain.increase_nb_mutation, True)

    # affiche l'intensiter de la mutation
    if (Constante.WITH_MUTATION):
      self.draw_text('I{}'.format(round(brain.mutation_intensity, 1)), FONT_WIDTH * 3, FONT_SIZE * 5.5)

    # dessine le graph
    self.displayGraph.draw( 
      brain.currentNeuralNetWeights
    )

    # applique le rendu
    pygame.display.update()

    # pour les button recupere le dernier etat du click de souri
    self.last_click_state = pygame.mouse.get_pressed()[0]

    

  def button(self, text, center_x, center_y, action=None, on_falling_edge=False):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    activate_action = click[0] == 1
    if (on_falling_edge):
      activate_action = click[0] == 1 != self.last_click_state
    x = center_x - FONT_WIDTH / 2 * len(text)
    width = FONT_WIDTH * len(text)
    y = center_y - FONT_SIZE / 2
    height = FONT_SIZE
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
      if activate_action and action != None:
        action()
    
    self.draw_text(text, center_x, center_y)

  def draw_text(self, text, center_x, center_y):
    textS = self.font.render(text, True, PURPLE)
    textSRect = textS.get_rect()
    textSRect.center = (center_x, center_y)
    self.window.blit(textS, textSRect)