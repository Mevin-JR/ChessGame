import pygame
import UI

chess_pieces = UI.chess_pieces
square_rects = UI.square_rects
all_pieces = UI.all_pieces

def get_square(mouse_pos: tuple) -> str:
    for square_coords, square_rect in square_rects.items():
        if square_rect.collidepoint(mouse_pos):
            return square_coords
    return None

def get_piece(mouse_pos: tuple):
    for piece_name, piece in chess_pieces.items():
        if piece.rect.collidepoint(mouse_pos):
            print("Selected: %s [%s]" % (piece_name, get_square(piece.rect.center))) # DEBUG
            return True, piece_name
    return False, None

def remove_piece(piece_name: str):
    all_pieces.remove(chess_pieces.get(piece_name))
    print("Removed: ", chess_pieces.get(piece_name)) # DEBUG
    del chess_pieces[piece_name]    

def own_piece(piece_name: str, target_name: str) -> bool:
    if target_name is None:
        return False
    return piece_name[0] == target_name[0]

def is_obstructed(start: str, dest: str) -> bool:
    if start[0] == dest[0]:
        direction = "v"
    elif start[1] == dest[1]:
        direction = "h"
    else:
        direction = "d"
    
    match direction:
        case "v":
            up_down_diff = 1 if int(start[1]) < int(dest[1]) else -1
            square_num = int(start[1]) + up_down_diff
            obstructed = False
            run = True
            while run:
                if square_num == int(dest[1]):
                    run = False
                    break
                square = f"{start[0]}{square_num}"
                for piece in chess_pieces.values():
                    if piece.rect.collidepoint(UI.get_square_center(square)):
                        run = False
                        obstructed = True
                square_num += up_down_diff
            return obstructed
        
        case "h":
            left_right_diff = 1 if ord(start[0]) < ord(dest[0]) else -1
            square_alph = ord(start[0]) + left_right_diff
            obstructed = False
            run = True
            while run:
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
        
def path_linear(start: str, dest: str) -> bool:
    return start[0] == dest[0] or start[1] == dest[1]

def path_diagonal(start: str, dest: str) -> bool:
    return start[0] != dest[0] and start[1] != dest[1]

def piece_can_move(piece_name_raw: str, dest: tuple) -> bool:
    current_square = get_square(chess_pieces.get(piece_name_raw).rect.center)
    dest_square = get_square(dest)
    if current_square == dest_square:
        return False
    
    piece = piece_name_raw[2:-1]
    match piece:
        case "pawn":
            return True
        case "rook":
            if path_linear(current_square, dest_square) and not is_obstructed(current_square, dest_square):
                return True
            print("Obstructed") # DEBUG
            return False
        case _:
            return False

def move_piece(current_piece: str, mouse_pos: tuple) -> None:
    piece_obj = chess_pieces.get(current_piece)
    rect: pygame.Rect = piece_obj.rect

    move_to_square = get_square(mouse_pos)
    move_to_square_center = UI.get_square_center(move_to_square)
    isOccupied, occupied_piece = get_piece(move_to_square_center)

    if not isOccupied and piece_can_move(current_piece, move_to_square_center):
        rect.center = move_to_square_center
        print("Moved: %s -> %s" % (current_piece, get_square(rect.center))) # DEBUG
    elif not piece_can_move(current_piece, move_to_square_center):
        return
    else:
        if not own_piece(current_piece, occupied_piece):
            remove_piece(occupied_piece)
            rect.center = move_to_square_center
            print("Moved: %s -> %s" % (current_piece, move_to_square)) # DEBUG
