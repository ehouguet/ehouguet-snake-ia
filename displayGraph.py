import pygame

PURPLE = (67,51,142)

class DisplayGraph:

  def __init__(self, window, pos_x, pos_y, width, height, names_input, names_output):
    self.window = window
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.width = width
    self.height = height
    self.names_input = names_input
    self.names_output = names_output

    # variable calcule
    self.input_space_between_node = height / len(names_input)
    self.output_space_between_node = height / len(names_output)
    self.radius = int(min(self.input_space_between_node, self.output_space_between_node) / 2 - 1)
    self.inputs_pos_x = self.pos_x + int(width / 4)
    self.inputs_text_pos_x = self.pos_x + int(width / 8)
    self.inputs_start_pos_y = (height - self.input_space_between_node * len(names_input)) / 2
    self.outputs_pos_x = self.pos_x + int(width * 3 / 4)
    self.outputs_text_pos_x = self.pos_x + int(width * 7 / 8)
    self.outputs_start_pos_y = (height - self.output_space_between_node * len(names_output)) / 2

    self.inputs_coordinate = [[
      int(self.inputs_pos_x), 
      int(self.inputs_start_pos_y + self.input_space_between_node * (idx + 0.5)),
    ] for idx, name in enumerate(self.names_input)]

    self.outputs_coordinate = [[
      int(self.outputs_pos_x), 
      int(self.outputs_start_pos_y + self.output_space_between_node * (idx + 0.5))
    ] for idx, name in enumerate(self.names_output)]
    
    # cree la font
    self.font = pygame.font.Font('freesansbold.ttf', self.radius + 2)

  def draw(self, neuralNet):
      
    # display lines
    for input_idx, input_coordinate in enumerate(self.inputs_coordinate):
      for output_idx, output_coordinate in enumerate(self.outputs_coordinate):
        weight = neuralNet.matrixInOut.matrix[output_idx][input_idx]
        color = (200, 200, 200)
        if (weight < 0):
          color = (200, 200 * (1 - abs(weight)), 200 * (1 - abs(weight)))
        if (weight > 0):
          color = (200 * (1 - weight), 200, 200 * (1 - weight))
        #print('color : {}'.format(int(3 * abs(weight) + 1)))
        pygame.draw.line(
          self.window, 
          color, 
          input_coordinate, 
          output_coordinate,
          int(3 * abs(weight) + 1))
          
    # affichage des noeuds d'inputs
    for idx, name_input in enumerate(self.names_input):
      pygame.draw.circle(
        self.window, 
        PURPLE, 
        self.inputs_coordinate[idx], 
        int(self.radius))
        
      self.draw_text(name_input, self.inputs_text_pos_x, self.inputs_coordinate[idx][1])
        
    # affichage des noeuds d'outputs
    for idx, name_output in enumerate(self.names_output):
      pygame.draw.circle(
        self.window, 
        PURPLE, 
        self.outputs_coordinate[idx], 
        int(self.radius))
        
      self.draw_text(name_output, self.outputs_text_pos_x, self.outputs_coordinate[idx][1])

  def draw_text(self, text, center_x, center_y):
    textS = self.font.render(text, True, PURPLE)
    textSRect = textS.get_rect()
    textSRect.center = (center_x, center_y)
    self.window.blit(textS, textSRect)
