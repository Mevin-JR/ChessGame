import pygame
import os
from typing import Tuple

# Chess board notations
# ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'], 
# ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'], 
# ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'], 
# ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'], 
# ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'], 
# ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'], 
# ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'], 
# ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

# Initialize var
files = os.listdir(os.path.join("assets", "chess_pieces"))
square_rects = {} # Global rects dictionaty
chess_pieces = {}
all_pieces = pygame.sprite.Group()
black = pygame.sprite.Group()
white = pygame.sprite.Group()

pieces_init_pos_black = {
    "b_rook1": "a8", "b_knight1": "b8", "b_bishop1": "c8", "b_queen0": "d8", "b_king0": "e8", "b_bishop2": "f8", "b_knight2": "g8", "b_rook2": "h8",
    "b_pawn1": "a7", "b_pawn2": "b7", "b_pawn3": "c7", "b_pawn4": "d7", "b_pawn5": "e7", "b_pawn6": "f7", "b_pawn7": "g7", "b_pawn8": "h7",
}

pieces_init_pos_white = {
    "w_pawn1": "a2", "w_pawn2": "b2", "w_pawn3": "c2", "w_pawn4": "d2", "w_pawn5": "e2", "w_pawn6": "f2", "w_pawn7": "g2", "w_pawn8": "h2",
    "w_rook1": "a1", "w_knight1": "b1", "w_bishop1": "c1", "w_queen0": "d1", "w_king0": "e1", "w_bishop2": "f1", "w_knight2": "g1", "w_rook2": "h1",
}

# Chess board UI
def chess_board(font: pygame.font.Font, offset_x: int, offset_y: int) -> Tuple[pygame.Surface, dict]:
    sq_dark = (184,139,74)
    sq_light = (227,193,111)
    square_size = 80
    square_rects.clear()

    # Surface
    board_surface = pygame.Surface((8 * square_size + 50, 8 * square_size + 50))
    board_surface.fill((50, 50, 50))

    for row in range(8):
        for col in range(8):
            color = sq_light if (row + col) % 2 == 0 else sq_dark
            rect = pygame.Rect(50 + col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(board_surface, color, rect)

            square_coord = f"{chr(97 + col)}{8 - row}"
            square_rects[square_coord] = rect

    add_notations(board_surface, font)

    # Adjust to offset
    count = 0
    for square_coord, square_rect in square_rects.items():
        square_rect.x +=  offset_x
        square_rect.y += offset_y
        if count == 63:
            break
        count += 1

    return board_surface, square_rects

def add_notations(board_surface: pygame.Surface, font: pygame.font.Font) -> None:
    square_size = 80
    y_num = 8
    y_left = 10
    y_top_init = 30

    x_alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    alph_count = 0
    x_left_init = 80
    x_top = 660

    for row in range(9):
        if row < 8:
            y_label = font.render(str(y_num), True, (255, 255, 255))
            board_surface.blit(y_label, (y_left, y_top_init))
            y_num -= 1
            y_top_init = 30 + (row + 1) * square_size
        else:
            for col in range(8):
                x_label = font.render(x_alph[alph_count], True, (255, 255, 255))
                board_surface.blit(x_label, (x_left_init, x_top))
                alph_count += 1
                x_left_init = 80 + (col + 1) * square_size

# Chess pieces
def get_black_pieces() -> dict:
    black_pieces = {}
    black_pieces_png = [png for png in files if "b_" in png]
    for piece in black_pieces_png:
        piece_name = piece[:-4]
        black_pieces[piece_name] = pygame.image.load(os.path.join("assets", "chess_pieces", piece)).convert_alpha()
    return black_pieces

def get_white_pieces() -> dict:
    white_pieces = {}
    white_pieces_png = [png for png in files if "w_" in png]
    for piece in white_pieces_png:
        piece_name = piece[:-4]
        white_pieces[piece_name] = pygame.image.load(os.path.join("assets", "chess_pieces", piece)).convert_alpha()
    return white_pieces

class Pieces(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

def get_square_center(square: str) -> tuple:
    rect: pygame.Rect = square_rects.get(square, None)
    if rect is not None:
        return rect.center
    return None

def initialize_pieces() -> Tuple[pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
    black_pieces = []
    black_pieces_raw = get_black_pieces()
    white_pieces = []
    white_pieces_raw = get_white_pieces()
    chess_pieces.clear()

    # Black Pieces
    for piece, square in pieces_init_pos_black.items():
        piece_obj = Pieces(black_pieces_raw.get(piece[:-1]), get_square_center(square))
        black_pieces.append(piece_obj)
        chess_pieces[piece] = piece_obj
    all_pieces.add(piece for piece in black_pieces)
    black.add(piece for piece in black_pieces)

    # White Pieces
    for piece, square in pieces_init_pos_white.items():
        piece_obj = Pieces(white_pieces_raw.get(piece[:-1]), get_square_center(square))
        white_pieces.append(piece_obj)
        chess_pieces[piece] = piece_obj
    all_pieces.add(piece for piece in white_pieces)
    white.add(piece for piece in white_pieces)

    return black, white, all_pieces
