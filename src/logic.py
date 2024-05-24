import pygame
import os

from utils import *
from pieces import *

# Sound fx's
pygame.mixer.init()
PIECE_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_move.wav"))
PIECE_CAPTURE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_capture.wav"))
ILLEGAL_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "illegal_move.wav"))

def remove_piece(piece_name: str) -> None: # Remove piece from board
    all_pieces_group.remove(chess_pieces_dict.get(piece_name)) # Remeving from group
    del chess_pieces_dict[piece_name] # Removing piece from dictionary

def capture_piece(piece_rect: pygame.Rect, target: str, target_square: tuple) -> None: # Handle piece capture
    remove_piece(target)
    piece_rect.center = target_square
    PIECE_CAPTURE_SOUND.play()

def piece_can_move(piece_name: str, dest: tuple) -> bool: # Check if piece can move (based on its characteristics)
    current_square = get_square(chess_pieces_dict.get(piece_name).rect.center)[0]
    dest_square = get_square(dest)[0]
    piece_name_formatted = piece_name[2:-1]

    if current_square == dest_square:
        return False
    
    piece_rect: pygame.Rect = chess_pieces_dict.get(piece_name).get_rect()
    piece_obj: Piece = PIECE_CLASS_DICT.get(piece_name_formatted)
    piece: Piece = piece_obj(piece_name, piece_rect.center, dest)

    moves = piece.get_allowed_moves()
    if moves:
        for move_list in moves.values():
            if dest_square in move_list:
                return True
    return False

def get_allowed_moves(piece_name: str, current_pos: tuple) -> dict: # Return available moves by the piece (move and captures)
    piece_name_formatted = piece_name[2:-1]
    piece_obj: Piece = PIECE_CLASS_DICT.get(piece_name_formatted)
    piece: Piece = piece_obj(piece_name, current_pos)
    moves = piece.get_allowed_moves()
    return moves

def move_piece(current_piece: str, mouse_pos: tuple) -> str:
    piece_sprite = chess_pieces_dict.get(current_piece)
    piece_rect: pygame.Rect = piece_sprite.get_rect()

    target_square = get_square(mouse_pos)[0]
    target_square_center = get_square_center(target_square)
    isOccupied = square_contains_piece(mouse_pos)
    can_move = piece_can_move(current_piece, target_square_center)

    if not can_move:
        ILLEGAL_MOVE_SOUND.play()
        return
    
    if not isOccupied:
        piece_rect.center = target_square_center
        PIECE_MOVE_SOUND.play()
        print("Moved: %s -> %s" % (current_piece, get_square(piece_rect.center)[0])) # DEBUG
    else:
        occupied_piece = get_piece_name(target_square_center)
        capture_piece(piece_rect, occupied_piece, target_square_center)
        print("Removed: ", occupied_piece) # DEBUG
    
    return f"{current_piece[2]}{target_square}"