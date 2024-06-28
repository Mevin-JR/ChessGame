import pygame

from utils import *
from pieces import *
from UI import *

queen_count = 1
positions_dict = {}

def add_queen(piece_name: str, pos: tuple) -> None:
    global queen_count
    if is_white(piece_name):
        piece_name_updated = "w_queen"
        piece_obj = Sprite(white_pieces_surface.get(piece_name_updated), pos)
        all_pieces_group.add(piece_obj)
        piece_name_count = f"{piece_name_updated}{queen_count}"
        queen_count += 1
        chess_pieces_dict[piece_name_count] = piece_obj
    else:
        piece_name_updated = "b_queen"
        piece_obj = Sprite(black_pieces_surface.get(piece_name_updated), pos)
        all_pieces_group.add(piece_obj)
        piece_name_count = f"{piece_name_updated}{queen_count}"
        queen_count += 1
        chess_pieces_dict[piece_name_count] = piece_obj

def remove_piece(piece_name: str) -> None: # Remove piece from board
    all_pieces_group.remove(chess_pieces_dict.get(piece_name)) # Remeving from group
    del chess_pieces_dict[piece_name] # Removing piece from dictionary

def capture_piece(piece_rect: pygame.Rect, target: str, target_square: tuple) -> None: # Handle piece capture
    remove_piece(target)
    piece_rect.center = target_square
    PIECE_CAPTURE_SOUND.play()

def piece_can_move(piece_name: str, dest: tuple) -> bool: # Check if piece can move (based on its characteristics)
    current_square = get_square_coord(chess_pieces_dict.get(piece_name).rect.center)
    dest_square = get_square_coord(dest)
    piece_name_formatted = piece_name[2:-1]
    can_move = False

    if current_square == dest_square:
        return False
    
    piece_rect: pygame.Rect = chess_pieces_dict.get(piece_name).get_rect()
    piece_obj: Piece = PIECE_CLASS_DICT.get(piece_name_formatted)
    piece: Piece = piece_obj(piece_name, piece_rect.center, dest)

    moves = piece.get_allowed_moves()
    if moves:
        for move_list in moves.values():
            if dest_square in move_list:
                can_move = True

    return can_move

def get_allowed_moves(piece_name: str, current_pos: tuple) -> dict: # Return available moves by the piece (move and captures)
    piece_name_formatted = piece_name[2:-1]
    piece_obj: Piece = PIECE_CLASS_DICT.get(piece_name_formatted)
    piece: Piece = piece_obj(piece_name, current_pos)
    moves = piece.get_allowed_moves()
    return moves

def can_promote(piece_name: str, current_pos: tuple):
    moves = get_allowed_moves(piece_name, current_pos)
    promotions = moves.get("promotions", [])
    if promotions:
        return True
    return False

def promote(piece_name: str, target_square: tuple):
    remove_piece(piece_name)
    add_queen(piece_name, target_square)
    PAWN_PROMOTION_SOUND.play()

def move_piece(current_piece: str, mouse_pos: tuple) -> str:
    piece_sprite: Sprite = chess_pieces_dict.get(current_piece)
    piece_rect: pygame.Rect = piece_sprite.get_rect()

    target_square = get_square_coord(mouse_pos)
    target_square_center = get_square_center(target_square)
    isOccupied = is_square_occupied(mouse_pos)
    can_move = piece_can_move(current_piece, target_square_center)

    if not can_move:
        ILLEGAL_MOVE_SOUND.play()
        return
    
    # Move or capture
    if not isOccupied:
        if can_promote(current_piece, piece_rect.center):
            promote(current_piece, target_square_center)
        else:
            piece_rect.center = target_square_center
            PIECE_MOVE_SOUND.play()
            print("Moved: %s -> %s" % (current_piece, get_square_coord(piece_rect.center))) # DEBUG
    else:
        if can_promote(current_piece, piece_rect.center):
            occupied_piece = get_piece_name(target_square_center)
            capture_piece(piece_rect, occupied_piece, target_square_center)
            promote(current_piece, target_square_center)
        else:
            occupied_piece = get_piece_name(target_square_center)
            capture_piece(piece_rect, occupied_piece, target_square_center)
            print("Removed: ", occupied_piece) # DEBUG
    
    update_positions()
    return f"{current_piece[2]}{target_square}"

def king_in_check() -> tuple[bool, dict]:
    in_check = False
    check_dict = {}
    for piece, moves in positions_dict.items():
        if moves is None:
            continue
        for square in moves:
            target_piece = get_piece_name(square)
            if target_piece is None:
                continue
            if "king" in target_piece and piece[0] != target_piece[0]:
                check_dict[target_piece] = piece
                in_check = True
    return in_check, check_dict

def update_positions():
    global positions_dict
    for piece, piece_obj in chess_pieces_dict.items():
        current_pos: pygame.Rect = piece_obj.get_rect()
        allowed_moves = get_allowed_moves(piece, current_pos.center)
        posiitons = []
        for value in allowed_moves.values():
            if value is not None:
                posiitons += value
        positions_dict[piece] = posiitons