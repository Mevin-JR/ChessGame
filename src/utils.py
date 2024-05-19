import pygame
import os

# Constants
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

FPS = 60

pygame.font.init()
FONT16 = pygame.font.Font(None, 16)
FONT32 = pygame.font.Font(None, 32)

# Chess board constants
BOARD_OFFSET_X, BOARD_OFFSET_Y = 50, 50

WHITE_START_POSITIONS = {
    "w_pawn1": "a2", "w_pawn2": "b2", "w_pawn3": "c2", "w_pawn4": "d2", "w_pawn5": "e2", "w_pawn6": "f2", "w_pawn7": "g2", "w_pawn8": "h2",
    "w_rook1": "a1", "w_knight1": "b1", "w_bishop1": "c1", "w_queen0": "d1", "w_king0": "e1", "w_bishop2": "f1", "w_knight2": "g1", "w_rook2": "h1",
}

BLACK_START_POSITIONS = {
    "b_rook1": "a8", "b_knight1": "b8", "b_bishop1": "c8", "b_queen0": "d8", "b_king0": "e8", "b_bishop2": "f8", "b_knight2": "g8", "b_rook2": "h8",
    "b_pawn1": "a7", "b_pawn2": "b7", "b_pawn3": "c7", "b_pawn4": "d7", "b_pawn5": "e7", "b_pawn6": "f7", "b_pawn7": "g7", "b_pawn8": "h7",
}

# Chess piece customizations
SQUARE_SIZE = 80
DARK_SQUARE_COLOR = (184, 139, 74)
LIGHT_SQUARE_COLOR = (227, 193, 111)

PIECE_FILES = os.listdir(os.path.join("assets", "chess_pieces"))