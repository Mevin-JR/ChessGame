import pygame
import os
from typing import overload

# Constants
GRAY = (50, 50, 50)
DARK_GRAY = (90, 90, 90)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

FPS = 60

pygame.font.init()
FONT16 = pygame.font.Font(None, 16)
FONT32 = pygame.font.Font(None, 32)

# Sound fx's
pygame.mixer.init()
PIECE_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_move.wav"))
PIECE_CAPTURE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_capture.wav"))
ILLEGAL_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "illegal_move.wav"))
PAWN_PROMOTION_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "pawn_promotion.wav"))

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

# Global variables
square_rects_dict, chess_pieces_dict = {}, {}
all_pieces_group = pygame.sprite.Group()

# Helper functions
@overload
def get_square(mouse_pos: tuple) -> tuple[str, pygame.Rect]: # get_square() Method overloading
    ...

@overload
def get_square(square_coords: str) -> pygame.Rect:
    ...

def get_square(arg):
    if isinstance(arg, tuple): # Check for input type
        for square_coords, square_rect in square_rects_dict.items():
            if square_rect.collidepoint(arg):
                return square_coords, square_rect
        return None, None
    elif isinstance(arg, str):
        return square_rects_dict.get(arg)
    else:
        raise ValueError("Argument must be a tuple or a string")

@overload
def get_piece_name(mouse_pos: tuple) -> str | None:
    ...

@overload
def get_piece_name(square: str) -> str | None:
    ...

def get_piece_name(arg):
    if isinstance(arg, tuple):
        if arg is not None:
            for piece_name, piece in chess_pieces_dict.items():
                if piece.rect.collidepoint(arg):
                    return piece_name
        return None
    elif isinstance(arg, str):
        if square_rects_dict.get(arg) is not None:
            square_center = get_square_center(arg)
            return get_piece_name(square_center)

@overload
def square_contains_piece(square_pos: tuple) -> bool:
    ...

@overload
def square_contains_piece(square_coord: str) -> bool:
    ...

def square_contains_piece(arg): # Checks if specified square holds a piece
    if isinstance(arg, tuple):
        square_rect = get_square(arg)[1]
        if square_rect is not None:
            for piece in chess_pieces_dict.values():
                if piece.rect.collidepoint(square_rect.center):
                    return True
        return False
    elif isinstance(arg, str):
        square_rect = get_square(arg)
        if square_rect is not None:
            for piece in chess_pieces_dict.values():
                if piece.rect.collidepoint(square_rect.center):
                    return True
        return False

def get_square_center(square: str) -> tuple:
    rect: pygame.Rect = square_rects_dict.get(square, None)
    if rect is not None:
        return rect.center # Position values of square center
    return None

def select_piece(mouse_pos: tuple) -> tuple[bool, str]:
    for piece_name, piece in chess_pieces_dict.items():
        if piece.rect.collidepoint(mouse_pos):
            return True, piece_name
    return False, None

def friendly_piece(current_square: str, target_square: str) -> bool: # Check if piece is friendly
    current_piece = get_piece_name(current_square)
    target_piece = get_piece_name(target_square)
    if target_piece is None:
        return False
    return current_piece[0] == target_piece[0] # TODO: Fix this abomination

def is_white(piece_name: str) -> bool: # Checks if piece is white
    return piece_name[0] == "w"

def has_moved(piece_name: str, current_square: str) -> bool:
    if is_white(piece_name):
        return WHITE_START_POSITIONS.get(piece_name) != current_square
    else:
        return BLACK_START_POSITIONS.get(piece_name) != current_square 