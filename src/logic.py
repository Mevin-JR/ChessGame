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
    print("Removed: ", chess_pieces_dict.get(piece_name)) # DEBUG
    del chess_pieces_dict[piece_name] # Removing piece from dictionary

def capture_piece(piece_rect: pygame.Rect, target: str, target_square: tuple) -> None: # Handle piece capture
    remove_piece(target)
    piece_rect.center = target_square
    PIECE_CAPTURE_SOUND.play()

def piece_can_move(piece_name_raw: str, dest: tuple) -> bool: # Check if piece can move (based on its characteristics)
    piece_name_formatted = piece_name_raw[2:-1]
    current_square = get_square(chess_pieces_dict.get(piece_name_raw).rect.center)[0]
    dest_square = get_square(dest)[0]
    piece_obj = chess_pieces_dict.get(piece_name_raw)
    piece_rect: pygame.Rect = piece_obj.get_rect()

    if current_square == dest_square:
        return False
    
    match piece_name_formatted:
        case "pawn":
            piece = Pawn(piece_name_raw, piece_rect.center, dest)
            can_move, moves = piece.get_allowed_moves()

            if can_move:
                for move_list in moves.values():
                    if dest_square in move_list:
                        return True
        case _:
            return False
    return False

def get_allowed_moves(piece_name: str, current_pos: tuple) -> dict:
    piece_name_formatted = piece_name[2:-1]
    moves = {}
    match piece_name_formatted:
        case "pawn":
            piece = Pawn(piece_name, current_pos)
            moves = piece.get_allowed_moves()[1]
    return moves

def move_piece(current_piece: str, mouse_pos: tuple) -> str:
    piece_obj = chess_pieces_dict.get(current_piece)
    rect: pygame.Rect = piece_obj.rect

    target_square = get_square(mouse_pos)[0]
    target_square_center = get_square_center(target_square)
    isOccupied, occupied_piece = select_piece(target_square_center) # Change this

    can_move = piece_can_move(current_piece, target_square_center)
    if not can_move:
        ILLEGAL_MOVE_SOUND.play()
        return
    
    if not isOccupied:
        rect.center = target_square_center
        PIECE_MOVE_SOUND.play()
        print("Moved: %s -> %s" % (current_piece, get_square(rect.center)[0])) # DEBUG
    else:
        capture_piece(rect, occupied_piece, target_square_center)
    
    return f"{current_piece[2]}{target_square}"