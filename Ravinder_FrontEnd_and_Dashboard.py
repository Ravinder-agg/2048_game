import pygame
from pygame.locals import *
import sys
import random

rows = 4
cols = 4
black = 0, 0, 0

PADDING = 10
TILE_SIZE = 125


pygame.init()
pygame.display.set_caption("2048")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    h_len = len(hex_color)
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))


class Board:
    def __init__(self, rows, cols, game_state, padding, tile_size, background_color, empty_tile_color,
                 background_tile_colors, tile_colors, font):
        self._rows = rows
        self._cols = cols
        self._padding = padding
        self._tile_size = tile_size
        self._background_color = background_color
        self._empty_tile_color = empty_tile_color
        self._background_tile_colors = background_tile_colors
        self._tile_colors = tile_colors
        self._font = pygame.font.SysFont(font[0], font[1], bold=True)
        self._width = cols*self._tile_size+(cols+1)*self._padding
        self._height = rows*self._tile_size+(rows+1)*self._padding
        self._grid = game_state
        self._surface = pygame.Surface((self._width, self._height))
        self._surface.fill(hex_to_rgb(self._background_color))

    def update_board(self, game_state):
        self._grid = game_state

    def draw_board(self):
        row = pygame.Surface((self._width, self._tile_size+self._padding), pygame.SRCALPHA, 32)
        row = row.convert_alpha()
        for col_num in range(self._cols):
            tile = pygame.Surface((self._tile_size, self._tile_size))
            tile.fill(hex_to_rgb(self._empty_tile_color))
            row.blit(tile, (self._padding+col_num*(self._padding+self._tile_size), self._padding))
        # Add as many empty rows to the board as the specified number of rows
        for row_num in range(self._rows):
            self._surface.blit(row, (0, (self._padding+self._tile_size)*row_num))

    def draw_tile(self, row, col, tile_value):
        tile = pygame.Surface((self._tile_size, self._tile_size))
        tile.fill(hex_to_rgb(self._background_tile_colors[tile_value]))
        text = self._font.render(str(tile_value), True, hex_to_rgb(self._tile_colors[tile_value]))
        text_width, text_height = text.get_size()
        tile.blit(text, ((self._tile_size-text_width)//2, (self._tile_size-text_height)//2))
        self._surface.blit(tile, (self._padding+(self._padding+self._tile_size)*col,
                                 self._padding+(self._padding+self._tile_size)*row))

    def draw_tiles(self):
        for row in range(self._rows):
            for col in range(self._cols):
                if self._grid[row][col] != 0:
                    self.draw_tile(row, col, self._grid[row][col])

    def get_board(self):
        return self._surface






BACKGROUND_COLOR = "#92877d"
BACKGROUND_COLOR_EMPTY_TILE = "#9e948a"
BACKGROUND_TILE_COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                          32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                          512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
TILE_COLORS = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
               32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
               512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40)


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}




def merge(line):
    n_elements = len(line)
    line = [value for value in line if value != 0]
    index = 0
    while index < len(line)-1:
        if line[index] == line[index+1]:
            line[index] *= 2
            line.pop(index+1)
        index += 1
    line += [0]*(n_elements-len(line))
    return line


class TwentyFortyEight:
    def __init__(self, grid_height, grid_width, offsets):
        self._offsets = offsets
        self._height = grid_height
        self._width = grid_width
        self._grid = None
        self.reset()
        self._initial_tiles = {UP: [(0, col, self._height) for col in range(self._width)],
                               DOWN: [(-1, col, self._height) for col in range(self._width)],
                               LEFT: [(row, 0, self._width) for row in range(self._height)],
                               RIGHT: [(row, -1, self._width) for row in range(self._height)]}

    def reset(self):
        self._grid = [[0]*self._width for dummy_i in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        return str(self._grid)

    def get_grid_height(self):
        return self._height

    def get_grid_width(self):
        return self._width

    def move(self, direction):
        moved = False
        displacement_vector = list(self._offsets[direction])
        initial_tiles = [list(initial_t) for initial_t in self._initial_tiles[direction]]
        for tile_pos in initial_tiles:
            to_merge = []
            for dummy_i in range(tile_pos[2]):
                to_merge += [self.get_tile(tile_pos[0], tile_pos[1])]
                tile_pos[0] += displacement_vector[0]
                tile_pos[1] += displacement_vector[1]
            merged = merge(to_merge)
            merged.reverse()
            for index in range(tile_pos[2]):
                tile_pos[0] -= displacement_vector[0]
                tile_pos[1] -= displacement_vector[1]
                if merged[index] != self.get_tile(tile_pos[0], tile_pos[1]):
                    moved = True
                self.set_tile(tile_pos[0], tile_pos[1], merged[index])
        if moved:
            self.new_tile()

    def new_tile(self):
        candidate_tiles = []
        for row_index in range(self._height):
            for col_index in range(self._width):
                if self._grid[row_index][col_index] == 0:
                    candidate_tiles += [(row_index, col_index)]
        if candidate_tiles:
            tile_pos = random.choice(candidate_tiles)
            tile_row, tile_col = tile_pos[0], tile_pos[1]
            tile_value = 2 if random.random() <= 0.9 else 4
            self.set_tile(tile_row, tile_col, tile_value)

    def set_tile(self, row, col, value):
        self._grid[row][col] = value

    def get_tile(self, row, col):
        return self._grid[row][col]

    def get_game_state(self):
        return self._grid






SIZE = width, height = cols * TILE_SIZE + (cols + 1) * PADDING,\
                       rows * TILE_SIZE + (rows + 1) * PADDING
screen = pygame.display.set_mode(SIZE)

twenty_forty_eight = TwentyFortyEight(rows, cols, OFFSETS)
board = Board(rows, cols, twenty_forty_eight.get_game_state(), PADDING, TILE_SIZE,
                BACKGROUND_COLOR, BACKGROUND_COLOR_EMPTY_TILE, BACKGROUND_TILE_COLORS,
                TILE_COLORS, FONT)

screen.fill(black)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                twenty_forty_eight.move(LEFT)
                board.update_board(twenty_forty_eight.get_game_state())
            elif event.key == pygame.K_RIGHT:
                twenty_forty_eight.move(RIGHT)
                board.update_board(twenty_forty_eight.get_game_state())
            elif event.key == pygame.K_UP:
                twenty_forty_eight.move(UP)
                board.update_board(twenty_forty_eight.get_game_state())
            elif event.key == pygame.K_DOWN:
                twenty_forty_eight.move(DOWN)
                board.update_board(twenty_forty_eight.get_game_state())

    board.draw_board()
    board.draw_tiles()
    screen.blit(board.get_board(), (0, 0))
    pygame.display.update()
    pygame.display.flip()
