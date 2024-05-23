import pygame
import os

from utils import *

class Sprite(pygame.sprite.Sprite): # Sprites class
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
    
    def get_rect(self) -> pygame.Rect:
        return self.rect

class UI: # User Interface class
    def __init__(self) -> None:
        # Instance varaible initialization
        self.white_pieces_surface = {}
        self.black_pieces_surface = {}
        self.board_surface = pygame.Surface(
            (8 * SQUARE_SIZE + 50, 8 * SQUARE_SIZE + 50)) # Chess board (whole)
    
    def chess_board(self) -> tuple[pygame.Surface, dict]:
        square_rects_dict.clear() # Reset rects dictionary
        self.board_surface.fill(GRAY)

        # Creating the 64 squares of the chess board
        for row in range(8):
            for col in range(8):
                square_color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
                square_rect = pygame.Rect(50 + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.board_surface, square_color, square_rect)
                square_coord = f"{chr(97 + col)}{8 - row}"
                square_rects_dict[square_coord] = square_rect # Storing square coords and rects

        self.add_notations() # Adding board notations

        # Adjusting to offset of the board
        count = 0
        for square_coord, square_rect in square_rects_dict.items():
            square_rect.x +=  BOARD_OFFSET_X
            square_rect.y += BOARD_OFFSET_Y
            if count == 63:
                break
            count += 1

        return self.board_surface, square_rects_dict

    def add_notations(self) -> None: # Board notations (Ranks & Files)
        # Ranks (Y axis)
        rank_left_margin = 10
        starting_rank = 8
        rank_top_margin = 30

        # Files (X axis)
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        file_count = 0
        file_top_margin = 660
        file_left_margin = 80

        for row in range(9):
            if row < 8:
                rank = FONT32.render(str(starting_rank), True, WHITE)
                self.board_surface.blit(rank, (rank_left_margin, rank_top_margin))

                rank_top_margin = 30 + (row + 1) * SQUARE_SIZE
                starting_rank -= 1 # Ranks in decreasing order (top - bottom)
            else:
                for col in range(8):
                    file = FONT32.render(files[file_count], True, WHITE)
                    self.board_surface.blit(file, (file_left_margin, file_top_margin))

                    file_left_margin = 80 + (col + 1) * SQUARE_SIZE
                    file_count += 1 # Files in alphabetic order (left - right)

    def load_white_pieces(self) -> None: # Loading image (Surface) of white pieces
        white_pieces_png = [png for png in PIECE_FILES if "w_" in png]
        for piece in white_pieces_png:
            piece_name = piece[:-4]
            self.white_pieces_surface[piece_name] = pygame.image.load(os.path.join("assets", "chess_pieces", piece)).convert_alpha()

    def load_black_pieces(self) -> None: # Loading image (Surface) of black pieces
        black_pieces_png = [png for png in PIECE_FILES if "b_" in png]
        for piece in black_pieces_png:
            piece_name = piece[:-4]
            self.black_pieces_surface[piece_name] = pygame.image.load(os.path.join("assets", "chess_pieces", piece)).convert_alpha()
    
    def initialize_pieces(self) -> pygame.sprite.Group: # Rendering pieces on chess board
        chess_pieces_dict.clear()

        # White Sprite
        self.load_white_pieces()
        for piece, square in WHITE_START_POSITIONS.items():
            piece_obj = Sprite(self.white_pieces_surface.get(piece[:-1]), get_square_center(square))
            chess_pieces_dict[piece] = piece_obj
            all_pieces_group.add(piece_obj) # Add piece in group

        # Black Sprite
        self.load_black_pieces()
        for piece, square in BLACK_START_POSITIONS.items():
            piece_obj = Sprite(self.black_pieces_surface.get(piece[:-1]), get_square_center(square))
            chess_pieces_dict[piece] = piece_obj
            all_pieces_group.add(piece_obj) # Add piece in group

        return all_pieces_group