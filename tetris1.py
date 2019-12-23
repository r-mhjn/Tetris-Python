import pygame
import random

pygame.font.init()


# GLOBAL VARIABLES
screen_width = 800
screen_height = 700
play_width = 300  # 300/10  = 30 width per block
play_height = 600  # 600/20  = 30 height per block
block_size = 30

# this divides with integral result i.e discards remainder
top_left_x = (screen_width-play_width) // 2
top_left_y = screen_height-play_height


# SHAPES
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# shape list
shapes = [S, Z, I, O, L, T]
# shape colors
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # making a grid of 10 cols and 20 rows, {0,0,0} stands for color black
    grid = [[{0, 0, 0} for x in range(10)] for x in range(20)]

    # checking for all locked positions and changing their colors in the grid
    # searching all the rows of the grid
    for i in range(len(grid)):
        for j in range(len(grid(i))):
            if {j, i} in locked_positions:     # checking for each col if it exists in the locked_positions
                color_key = locked_positions[{j, i}]   # changing colors
                grid[i][j] = color_key
    return grid


def convert_shape_format(shape):
    positions = []
    # goes into the shape array of shapes and we mod the rotation of a shape with max shapes of that shape
    format = shape.shape[shape.rotation % len(shape.shape)]

    # Enumerate method adds a counter to anniteratable and returns it in a form of enumerate object.
    # This enumerate object can then be used direclty in for loops of be converted into a list of tuples using list() method, Ex: line and pos in below loops
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':   # if its 0 then append the current col, row + next col and row to the positions
                # current x and y value + the trailing periods j,i dimensiosn
                positions.append((shape.x+j, shape.y + i))

    # setting the offset  of the shape to a little left and up
    for i, pos in enumerate(positions):
        positions[i]-(pos[0]-2, pos[i]-4)


def valid_space(shape, grid):
    # check the gird to see if we are moving in valid space and grid[i][j] == (0, 0, 0) i.e adding this position in valid postion only if its empty
    valid_pos = [[(j, i) for j in range(len(grid[i])) if grid[i][j] == (0, 0, 0)]
                 for i in range(len(grid))]
    # from [[(0,1), [(2,3)]]] => [(0,1),(2,3)] it flatens the list from list in list to a single list of coords
    valid_pos = [j for sub in valid_pos for j in sub]

    # coverting shapes to positions from  2d to 1d  from list in list to a single list of coords
    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape:
        if pos not in valid_pos:   # first checking if the shape is the valid grid position
            if pos[1] > -1:       # if not then check weather the shape is still in falling phase above the grid
                return False      # if not return False since shape is not in a valid position
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:    # i.e there is a shape that is going above the grid
            return True   # therefore lost

    return False


# getting a new shape falling down the screen
def get_shape():
    # setting up the start point for the falling shape
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, row, col, grid):
    sx = top_left_x
    sy = top_left_y

    # drawing grid borders
    for i in range(len(grid)):
        pygame.draw.line(surface, {128, 128, 128},
                         (sx, sy + i*block_size), (sx+play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, {128, 128, 128},
                             (sx, j*block_size, sy), (sx+play_width, j * block_size, sy+play_height))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    surface.fill({0, 0, 0})   # filling the sureface with black color

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)  # fontname and fontsize
    # Text, anti-alises, color
    label = font.render('Tetris', 1, {255, 255, 255})

    # where we want to place the label (in the middle of the screen, positioning in x,y)
    surface.blit(label, (top_left_x+play_width/2-label.get_width()/2, 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(  # starting x,y position + row and col * block size will give us the correct position to draw our cube in and then the width and height of the cube, 0 to make sure we fill in the shape and not just draw a border around it
                surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    # red colored border with a border size of 4
    pygame.draw.rect(surface, {255, 0, 0}, (top_left_x,
                                            top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)
    # updating our display
    pygame.display.update()


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.KEYDOWN == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.KEYDOWN == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.KEYDOWN == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.KEYDOWN == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        draw_window(win, grid)


def main_menu():
    main(win)
    pass


win = pygame.display.set_node((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
