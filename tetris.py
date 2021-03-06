#!/usr/bin/env python3
import pygame
import random
import time

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

L = [['.)....',
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
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    # checking for all locked positions and changing their colors in the grid
    # searching all the rows of the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:     # checking for each col if it exists in the locked_positions
                color_key = locked_positions[(j, i)]   # changing colors
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
        positions[i] = (pos[0]-2, pos[1]-4)

    return positions


def valid_space(shape, grid):
    # check the gird to see if we are moving in valid space and grid[i][j] == (0, 0, 0) i.e adding this position in valid postion only if its empty
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                 for i in range(20)]
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


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width // 2 - int(label.get_width()//2),
                         top_left_y + play_height//2 - label.get_height()//2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # drawing grid borders
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i*block_size), (sx+play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j*block_size, sy), (sx + j * block_size, sy+play_height))


def clear_rows(grid, locked_positions):

    inc = 0
    # loops throught the grid backwards
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]  # setting row to every row in the grid
        if (0, 0, 0) not in row:  # if no black square in row i.e the row has not empty squares
            inc += 1
            ind = i
            # now we loop through the cols of that row and try to delete every col from the locked_positions
            for j in range(len(row)):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue

    # now we need to shift every row i,e if we delete a bottom row every row above needs to come down by one
    # but in our case we are removing an entire row from the grid so we need to add a new row at the top of the grid

    # given a list like [(0,1), (0,0)] ->[(0,0), (0,1)]to get all the positons that have the same y value in the correct order
    if inc > 0:
        # for every key in our sorted list of locked position based on the y value
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key  # getting x,y of each key in lockec_positions
            if y < ind:  # if y value of the key is above the current index of the row we removed
                newKey = (x, y+inc)  # adding the the y valueto shift it down
                locked_positions[newKey] = locked_positions.pop(key)

    return inc


def draw_next_shape(shape, surface):
    # draws the next shape to come
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # Now to set position for the label
    sx = top_left_x + play_width+60
    sy = top_left_y + play_height//2 - 100

    # fetching the shape to draw
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':  # if its the shape then draw
                pygame.draw.rect(surface, shape.color, (sx+j*block_size,
                                                        sy+i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx+10, sy-30))


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))   # filling the surface with black color

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)  # fontname and fontsize

    # setting up current score label
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: '+str(score), 1, (255, 255, 255))
    # Now to set position for score
    sx = top_left_x + play_width+60
    sy = top_left_y + play_height//2 - 100
    surface.blit(label, (sx+20, sy+160))

    # setting up maxscore label
    label = font.render('High Score: '+str(last_score), 1, (255, 255, 255))
    # Now to set position for maxscore
    sx = top_left_x - 200
    sy = top_left_y + 200
    surface.blit(label, (sx+20, sy+160))

    # draws shape
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(  # starting x,y position + row and col * block size will give us the correct position to draw our cube in and then the width and height of the cube, 0 to make sure we fill in the shape and not just draw a border around it
                surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    # red colored border with a border size of 4
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                                            top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    # updating our display
    pygame.display.update()


def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()  # to remove \n

    return score


def pause_game(surface):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)  # fontname and fontsize

    # setting up current score label
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render("Paused", 1, (255, 255, 255))
    # Now to set position for score
    sx = top_left_x + play_width+60
    sy = top_left_y + play_height//2 - 100
    surface.blit(label, (sx+20, sy+80))


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    last_score = max_score()

    while run:
        # updating grid every time we move
        grid = create_grid(locked_positions)
        # it gets the amount of time since last clock.tick()
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1  # if we move into a valid position by above action then revert
                # its going to lock the the shape piece and make another shape come down the screen
                change_piece = True

        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE:
                    pause_game(win)

        # to check all the positions of the shape to check if we have hit the ground or to see if we have to lock it
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # if the shape is not above the screen the we give the shape a color
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # when we pass locked postions in grid we get each of those positions and then update the color of grid
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()   # get a new shape
            change_piece = False  # since now we have a new shape so change_piece = False
            # checking for clear row very time a block hits the ground
        score += clear_rows(grid, locked_positions)*10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # check is we have lost the game
        if check_lost(locked_positions):
            draw_text_middle(win, "You Lost!!!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):

    run = True
    pygame.init()
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any key to play", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     # if person hits exit then we quit the game
                run = False
            if event.type == pygame.KEYDOWN:  # if person hits any other key we start the game loop
                main(win)

    pygame.display.quit()

    main(win)


icon = pygame.image.load('tetris_icon.png')
pygame.display.set_icon(icon)
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
