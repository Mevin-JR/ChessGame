import pygame
import os
from typing import overload

from utils import WHITE_START_POSITIONS, BLACK_START_POSITIONS
import UI

# Sound fx's
pygame.mixer.init()
PIECE_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_move.wav"))
PIECE_CAPTURE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "piece_capture.wav"))
ILLEGAL_MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound_fx", "illegal_move.wav"))

# Variable initialization
square_rects = UI.square_rects_dict
chess_pieces = UI.chess_pieces_dict
all_pieces = UI.all_pieces_group

@overload
def get_square(mouse_pos: tuple) -> tuple[str, pygame.Rect]: # get_square() Method overloading
    ...

@overload
def get_square(square_coords: str) -> pygame.Rect:
    ...

def get_square(arg):
    if isinstance(arg, tuple): # Check for input type
        for square_coords, square_rect in square_rects.items():
            if square_rect.collidepoint(arg):
                return square_coords, square_rect
        return None, None
    elif isinstance(arg, str):
        return square_rects.get(arg)
    else:
        raise ValueError("Argument must be a tuple or a string")

def square_contains_piece(square: str) -> bool: # Checks if specified square holds a piece
    square_rect = get_square(square)
    if square_rect is None:
        return False
    for piece in chess_pieces.values():
        if piece.rect.collidepoint(square_rect.center):
            return True
    return False

def get_piece(mouse_pos: tuple) -> tuple[bool, str]:
    for piece_name, piece in chess_pieces.items():
        if piece.rect.collidepoint(mouse_pos):
            print("Selected: %s [%s]" % (piece_name, get_square(piece.rect.center)[0])) # DEBUG
            return True, piece_name
    return False, None

def is_white(piece_name: str) -> bool: # Checks if piece is white
    return piece_name[0] == "w"

def remove_piece(piece_name: str) -> None: # Remove piece from board
    all_pieces.remove(chess_pieces.get(piece_name)) # Remeving from group
    print("Removed: ", chess_pieces.get(piece_name)) # DEBUG
    del chess_pieces[piece_name] # Removing piece from dictionary

def capture_piece(piece_rect: pygame.Rect, target: str, target_square: tuple) -> None: # Handle piece capture
    remove_piece(target)
    piece_rect.center = target_square
    PIECE_CAPTURE_SOUND.play()

def friendly_piece(piece_name: str, target_name: str) -> bool: # Check if piece is friendly
    if target_name is None:
        return False
    return piece_name[0] == target_name[0]

def path_linear(start: str, dest: str) -> bool: # Check if piece path is linear (vertical or horizontal)
    return start[0] == dest[0] or start[1] == dest[1]

def path_diagonal(start: str, dest: str) -> bool: # Check if piece path is diagonal
    return start[0] != dest[0] and start[1] != dest[1]

def is_obstructed(start: str, dest: str) -> bool: # Check for obstruction
    # Classify piece path (vertical, horizontal, diagonal)
    if start[0] == dest[0]:
        direction = "v"
    elif start[1] == dest[1]:
        direction = "h"
    else:
        direction = "d"
    
    match direction:
        # Vertical path
        case "v":
            up_down_diff = 1 if int(start[1]) < int(dest[1]) else -1
            square_num = int(start[1]) + up_down_diff
            obstructed = False
            run = True
            while run:
                if square_num > int(dest[1]) or square_num < int(dest[1]):
                    run = False
                    break
                square = f"{start[0]}{square_num}"
                print("Check: ", square)
                for piece in chess_pieces.values():
                    if piece.rect.collidepoint(UI.get_square_center(square)):
                        run = False
                        obstructed = True
                square_num += up_down_diff
            return obstructed
        
        # Horizontal path
        case "h":
            left_right_diff = 1 if ord(start[0]) < ord(dest[0]) else -1
            square_alph = ord(start[0]) + left_right_diff
            obstructed = False
            run = True
            while run or obstructed is True:
                if chr(square_alph) == dest[0]:
                    run = False
                    break
                square = f"{chr(square_alph)}{start[1]}"
                for piece in chess_pieces.values():
                    if piece.rect.collidepoint(UI.get_square_center(square)):
                        run = False
                        obstructed = True
                square_alph += left_right_diff
            return obstructed

def piece_can_move(piece_name_raw: str, dest: tuple) -> bool: # Check if piece can move (based on its characteristics)
    current_square = get_square(chess_pieces.get(piece_name_raw).rect.center)[0]
    dest_square = get_square(dest)[0]
    if current_square == dest_square:
        return False
    
    piece_obj: UI.Pieces = chess_pieces.get(piece_name_raw)
    piece_rect: pygame.Rect = piece_obj.get_rect()
    piece = piece_name_raw[2:-1]
    match piece:
        case "pawn":
            if is_obstructed(current_square, dest_square):
                return False
            init_pos: dict = BLACK_START_POSITIONS if not is_white(piece_name_raw) else WHITE_START_POSITIONS
            has_moved = True if get_square(piece_rect.center)[0] != init_pos.get(piece_name_raw) else False
            if has_moved:
                if current_square[0] == dest_square[0]: # Only vertical movement
                    if is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) + 1: # Prevent moving back (white)
                        return True
                    if not is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) - 1: # Prevent moving back (black)
                        return True
                elif path_diagonal(current_square, dest_square):
                    if is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) + 1:
                        return square_contains_piece(dest_square)
                    if not is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) - 1:
                        return square_contains_piece(dest_square)
            else:
                if current_square[0] == dest_square[0]:
                    if is_white(piece_name_raw): # 2 square movement (white)
                        if int(dest_square[1]) == int(current_square[1]) + 1:
                            return True
                        elif int(dest_square[1]) == int(current_square[1]) + 2:
                            intermediate_square = f"{dest_square[0]}{int(dest_square[1]) - 1}"
                            return not square_contains_piece(dest_square) and not square_contains_piece(intermediate_square)
                    if not is_white(piece_name_raw): # 2 square movement (black)
                        if int(dest_square[1]) == int(current_square[1]) - 1:
                            return True
                        elif int(dest_square[1]) == int(current_square[1]) - 2:
                            intermediate_square = f"{dest_square[0]}{int(dest_square[1]) + 1}"
                            return not square_contains_piece(dest_square) and not square_contains_piece(intermediate_square)
                        return True
                elif path_diagonal(current_square, dest_square):
                    if is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) + 1:
                        return square_contains_piece(dest_square)
                    if not is_white(piece_name_raw) and int(dest_square[1]) == int(current_square[1]) - 1:
                        return square_contains_piece(dest_square)
            return False
        case "rook":
            if path_linear(current_square, dest_square) and not is_obstructed(current_square, dest_square):
                return True
        case _:
            return False
    return False

def move_piece(current_piece: str, mouse_pos: tuple) -> str:
    piece_obj = chess_pieces.get(current_piece)
    rect: pygame.Rect = piece_obj.rect

    move_to_square = get_square(mouse_pos)[0]
    move_to_square_center = UI.get_square_center(move_to_square)
    isOccupied, occupied_piece = get_piece(move_to_square_center)

    if not piece_can_move(current_piece, move_to_square_center):
        ILLEGAL_MOVE_SOUND.play()
        return
    
    if not isOccupied:
        rect.center = move_to_square_center
        PIECE_MOVE_SOUND.play()
        print("Moved: %s -> %s" % (current_piece, get_square(rect.center)[0])) # DEBUG
    else:
        capture_piece(rect, occupied_piece, move_to_square_center)
    
    return f"{current_piece[2]}{move_to_square}"

def get_allowed_moves(piece_name: str) -> dict:
    piece = piece_name[2:-1]
    piece_rect: pygame.Rect = chess_pieces.get(piece_name).get_rect()

    moves = {"up": None, "down": None, "dl_up": None, "dl_down": None, "dr_up": None, "dr_down": None}
    capture_moves = {"up": None, "down": None, "dl_up": None, "dl_down": None, "dr_up": None, "dr_down": None}
    moves_list = []
    match piece:
        case "pawn":
            square_coords_0 = get_square(piece_rect.center)[0]

            init_pos: dict = BLACK_START_POSITIONS if not is_white(piece_name) else WHITE_START_POSITIONS
            has_moved = True if square_coords_0 != init_pos.get(piece_name) else False
            
            if is_white(piece_name):
                if has_moved:
                    differential = 1
                else:
                    differential = 2
                for i in range(1, differential + 1):
                    coord_y = int(square_coords_0[1]) + i
                    if coord_y > 8: # Out of bounds
                        moves_list = []
                        break
                    square_coords_1 = f"{square_coords_0[0]}{coord_y}"
                    if square_contains_piece(square_coords_1):
                        break
                    moves_list.append(get_square(square_coords_1))
                moves["up"] = moves_list
                dl_up = f"{chr(ord(square_coords_0[0]) - 1)}{int(square_coords_0[1]) + 1}"
                dr_up = f"{chr(ord(square_coords_0[0]) + 1)}{int(square_coords_0[1]) + 1}"
                if square_contains_piece(dl_up):
                    capture_moves["dl_up"] = [get_square(dl_up)]
                if square_contains_piece(dr_up):
                    capture_moves["dr_up"] = [get_square(dr_up)]
            else:
                if has_moved:
                    differential = -1
                else:
                    differential = -2
                for i in range(1, abs(differential) + 1):
                    coord_y = int(square_coords_0[1]) - i
                    if coord_y < 1: # Out of bounds
                        moves_list = []
                        break
                    square_coords_1 = f"{square_coords_0[0]}{coord_y}"
                    if square_contains_piece(square_coords_1):
                        break
                    moves_list.append(get_square(square_coords_1))
                moves["down"] = moves_list
                dl_down = f"{chr(ord(square_coords_0[0]) - 1)}{int(square_coords_0[1]) - 1}"
                dr_down = f"{chr(ord(square_coords_0[0]) + 1)}{int(square_coords_0[1]) - 1}"
                if square_contains_piece(dl_down):
                    capture_moves["dl_down"] = [get_square(dl_down)]
                if square_contains_piece(dr_down):
                    capture_moves["dr_down"] = [get_square(dr_down)]
        case "king":
            pass
        case _:
            pass
    return moves, capture_moves