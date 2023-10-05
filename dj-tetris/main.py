import pygame
from enum import Enum
from random import choice

BLOCK_SIZE = 30
ROWS = 20
COLS = 10
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
GAME_WIDTH = BLOCK_SIZE * COLS
GAME_HEIGHT = BLOCK_SIZE * ROWS
GAME_TOP_X = (SCREEN_WIDTH // 2) - GAME_WIDTH // 2
GAME_TOP_Y = (SCREEN_HEIGHT // 2) - GAME_HEIGHT // 2

window = None

COLOR_GRAY = pygame.color.Color(128, 128, 128)


class TileTypes(Enum):
    EMPTY = 0
    O_TETROMINO = 1
    I_TERTOMINO = 2
    T_TERTOMINO = 3
    L_TERTOMINO = 4
    J_TERTOMINO = 5
    S_TERTOMINO = 6
    Z_TERTOMINO = 7

    @property
    def color(self):
        return TileColors[self]


TileColors = {
    TileTypes.EMPTY: pygame.color.Color(0, 0, 0, 0),
    TileTypes.O_TETROMINO: pygame.color.Color(255, 255, 0),
}


class Rotation(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Tertomino:
    def __init__(self, column: int, row: int, shape: TileTypes):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape.color
        self.rotation = Rotation.NORTH


def getDropSpeed(level):
    l = level - 1
    return (0.8 - (l * 0.007)) ** l


def drawGrid():
    global window
    x = GAME_TOP_X
    y = GAME_TOP_Y

    for r in range(ROWS + 1):
        pygame.draw.line(
            window,
            COLOR_GRAY,
            (x, y + r * 30),
            (x + GAME_WIDTH, y + r * 30),
        )

        for c in range(COLS + 1):
            pygame.draw.line(
                window,
                COLOR_GRAY,
                (x + c * 30, y),
                (x + c * 30, y + GAME_HEIGHT),
            )


lockedMinos = {
    (4, 12): COLOR_GRAY,
}


def getBoard():
    board = [[pygame.color.Color(0, 0, 0, 0) for _ in range(20)] for _ in range(10)]

    for (x, y), color in lockedMinos.items():
        board[x][y] = color

    return board


def getNextTertomino():
    return Tertomino(
        5,
        20,
        choice(
            [
                TileTypes.O_TETROMINO,
                TileTypes.I_TERTOMINO,
                TileTypes.T_TERTOMINO,
                TileTypes.L_TERTOMINO,
                TileTypes.J_TERTOMINO,
                TileTypes.S_TERTOMINO,
                TileTypes.Z_TERTOMINO,
            ]
        ),
    )


def main():
    global window

    [print(l, getDropSpeed(l)) for l in range(1, 25)]
    pygame.init()
    pygame.display.set_caption("DJ Tertis")
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    timeFallen = 0
    fastFall = False

    gameRunning = True

    while gameRunning:
        timeFallen += clock.get_rawtime() * (1 if fastFall else 20)
        clock.tick()

        board = getBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False

        drawGrid()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
