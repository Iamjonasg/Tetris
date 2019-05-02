import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 30 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):

    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] ==(0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):

    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height() / 2))


def draw_under_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height() / 2 + 50))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy+i*block_size), (sx + play_width, sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next", 1, (0, 0, 0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 55, sy - 30))


def draw_level(surface, one_level):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Level: " + str(one_level), 1, (0, 0, 0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 40, sy + 250))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background("Ed.jpg", [0, 0])


def draw_window(surface, grid, score=0):

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (0, 0, 0))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (0, 0, 0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 40, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)


def draw_hold(shape, surface):

    sx = top_left_x + play_width - 500
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)


def draw_hold_text(surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Hold", 1, (0, 0, 0))

    sx = top_left_x + play_width - 500
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 55, sy - 30))


def update_score(nscore):
    with open("Scores.txt", 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open("Scores.txt", "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open("Scores.txt", 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def main(surface, level, fall_speed):
    has_held = False
    locked_positions = {}
    change_piece = False
    run1 = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0
    move_left = False
    move_right = False
    move_down = False
    has_not_switched = True
    timer_left = 0
    timer_down = 0
    timer_right = 0
    lines_cleared = 0
    while run1:
        surface.fill([255, 255, 255])
        surface.blit(BackGround.image, BackGround.rect)

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        timer_left += 1
        timer_down += 1
        timer_right += 1
        change_level = False

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if current_piece.y > 2:
                        current_piece.x -= 1
                    move_left = True
                    timer_left = 0
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_d:
                    if current_piece.y > 2:
                        current_piece.x += 1
                    move_right = True
                    timer_right = 0
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        move_right = False

                if event.key == pygame.K_s:
                    if current_piece.y > 2:
                        current_piece.y += 1
                    move_down = True
                    timer_down = 0
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                        move_down = False

                if event.key == pygame.K_w:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

                if event.key == pygame.K_q and has_not_switched:

                    has_not_switched = False
                    if not has_held:
                        held_piece = current_piece
                        current_piece = next_piece
                        next_piece = get_shape()
                        has_held = True
                        current_piece.x = 5
                        current_piece.y = 0
                    else:
                        new_held_piece = current_piece
                        current_piece = held_piece
                        held_piece = new_held_piece
                        current_piece.x = 5
                        current_piece.y = 0
            else:
                move_right = False
                move_left = False
                move_down = False

        if move_left and current_piece.y > 2 and timer_left > 8:
            timer_left = 0
            current_piece.x -= 1
            if not (valid_space(current_piece, grid)):
                current_piece.x += 1
                move_left = False
        elif move_right and current_piece.y > 2 and timer_right > 8:
            timer_right = 0
            current_piece.x += 1
            if not (valid_space(current_piece, grid)):
                current_piece.x -= 1
                move_right = False

        elif move_down and current_piece.y > 2 and timer_down > 6:
            timer_down = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)):
                current_piece.y -= 1
                move_down = False

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            lines = clear_rows(grid, locked_positions)
            if lines == 1:
                score += 40*(level + 1)
            if lines == 2:
                score += 100*(level + 1)
            if lines == 3:
                score += 300*(level + 1)
            if lines == 4:
                score += 1200*(level + 1)
            lines_cleared += lines
            has_not_switched = True
            if lines == 1 and lines_cleared % 10 == 0:
                level += 1
            if lines == 2 and lines_cleared % 10 == 1:
                level += 1
            if lines == 3 and lines_cleared % 10 == 2:
                level += 1
            if lines == 4 and lines_cleared % 10 == 3:
                level += 1
                change_level = True

        if change_level:
            if 0 < level <= 8:
                fall_speed -= 0.083
            if level == 9:
                fall_speed -= 0.04
            if level in (10, 13, 19, 29):
                fall_speed -= 0.02

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        draw_level(win, level)
        draw_hold_text(win)
        try:
            draw_hold(held_piece, win)
        except:
            pass
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("LOLTMORT", 80, (255, 255, 255), win)
            draw_under_middle("Lines cleared: " + str(lines_cleared), 60, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run1 = False
            update_score(score)


def main_menu(surface):
    run = True
    while run:
        high_score = max_score()
        surface.fill((0, 0, 0))
        draw_text_middle("Enter your starting level(0-9)", 60, (255, 255, 255), win)
        draw_under_middle("Highscore: " + str(high_score), 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    main(win, 0, 0.8)
                elif event.key == pygame.K_1:
                    main(win, 1, 0.717)
                elif event.key == pygame.K_2:
                    main(win, 2, 0.633)
                elif event.key == pygame.K_3:
                    main(win, 3, 0.55)
                elif event.key == pygame.K_4:
                    main(win, 4, 0.477)
                elif event.key == pygame.K_5:
                    main(win, 5, 0.383)
                elif event.key == pygame.K_6:
                    main(win, 6, 0.3)
                elif event.key == pygame.K_7:
                    main(win, 7, 0.217)
                elif event.key == pygame.K_8:
                    main(win, 8, 0.133)
                elif event.key == pygame.K_9:
                    main(win, 9, 0.1)
                else:
                    continue

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game
