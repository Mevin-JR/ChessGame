from utils import *

# Abstract piece class
class Piece:
    def __init__(self, piece_name: str, current_pos: tuple, dest_pos: tuple = None) -> None:
        self.piece_name = piece_name
        self.current_pos = current_pos
        self.dest_pos = dest_pos
        self.moves = {}
        self.capture_moves = []

    def get_allowed_moves(self) -> dict:
        raise NotImplementedError("This method must be overridden in derived classes")

class Pawn(Piece):
    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        starting_rank = int(current_square[1])

        direction = 1 if is_white(self.piece_name) else -1

        if has_moved(self.piece_name, current_square):
            next_square_rank = starting_rank + direction
            next_square_coord = f"{current_square[0]}{next_square_rank}"

            if square_rects_dict.get(next_square_coord) is not None and not square_contains_piece(next_square_coord):
                self.moves["moves"] = [next_square_coord]

        else:
            forward_moves = []
            direction_2 = direction

            for i in range(2):
                next_square_rank = starting_rank + direction_2
                next_square_coord = f"{current_square[0]}{next_square_rank}"

                if i == 0 and square_contains_piece(next_square_coord):
                    forward_moves = []
                    break

                if square_rects_dict.get(next_square_coord) is not None and not square_contains_piece(next_square_coord):
                    forward_moves.append(next_square_coord)
                
                direction_2 = direction_2 + 1 if is_white(self.piece_name) else direction_2 - 1

            if forward_moves:
                self.moves["moves"] = forward_moves

        capture_moves = self.get_capture_moves(current_square, direction)
        if capture_moves:
            self.moves["capture"] = [move for move in capture_moves]
        
        return self.moves

    def get_capture_moves(self, current_square: str, direction: int) -> list:
        left_diagonal = f"{chr(ord(current_square[0]) - 1)}{int(current_square[1]) + direction}"
        right_diagonal = f"{chr(ord(current_square[0]) + 1)}{int(current_square[1]) + direction}"

        if square_rects_dict.get(left_diagonal) is not None and square_contains_piece(left_diagonal) and not friendly_piece(current_square, left_diagonal):
            self.capture_moves.append(left_diagonal)
        if square_rects_dict.get(right_diagonal) is not None and square_contains_piece(right_diagonal) and not friendly_piece(current_square, right_diagonal):
            self.capture_moves.append(right_diagonal)    
            
        return self.capture_moves

class Rook(Piece):
    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]

        file = current_square[0]
        starting_file = ord(current_square[0])
        rank = int(current_square[1])
        starting_rank = int(current_square[1])

        moves_list = []
        for square_rank in range(starting_rank + 1, 9):
            next_coord = f"{file}{square_rank}"
            if not square_contains_piece(next_coord):
                moves_list.append(next_coord)
            else:
                if not friendly_piece(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                break
        
        for square_rank in range(starting_rank - 1, 0, -1):
            next_coord = f"{file}{square_rank}"
            if not square_contains_piece(next_coord):
                moves_list.append(next_coord)
            else:
                if not friendly_piece(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                break

        for file_unicode in range(starting_file + 1, 105, 1):
            next_coord = f"{chr(file_unicode)}{rank}"
            if not square_contains_piece(next_coord):
                moves_list.append(next_coord)
            else:
                if not friendly_piece(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                break
        
        for file_unicode in range(starting_file - 1, 96, -1):
            next_coord = f"{chr(file_unicode)}{rank}"
            if not square_contains_piece(next_coord):
                moves_list.append(next_coord)
            else: 
                if not friendly_piece(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                break
                
        self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["capture"] = self.capture_moves

        return self.moves
    
class Bishop(Piece):
    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]

        file = ord(current_square[0])
        rank = int(current_square[1])

        temp_file = file
        temp_rank = rank
        
        moves_list = []
        for i in range(1, 8):
            temp_file, temp_rank = temp_file + 1, temp_rank + 1
            if temp_file > 104 or temp_rank > 8:
                break
            right_up_coord = f"{chr(temp_file)}{temp_rank}"
            obstructed = add_move(current_square, right_up_coord, moves_list, self.capture_moves)
            if obstructed:
                break
        
        temp_file = file
        temp_rank = rank

        for i in range(1, 8):
            temp_file, temp_rank = temp_file - 1, temp_rank - 1
            if temp_file < 97 or temp_rank < 1:
                break
            left_down_coord = f"{chr(temp_file)}{temp_rank}"
            obstructed = add_move(current_square, left_down_coord, moves_list, self.capture_moves)
            if obstructed:
                break
        
        temp_file = file
        temp_rank = rank

        for i in range(1, 8):
            temp_file, temp_rank = temp_file - 1, temp_rank + 1
            if temp_file < 97 or temp_rank > 8:
                break
            left_up_coord = f"{chr(temp_file)}{temp_rank}"
            obstructed = add_move(current_square, left_up_coord, moves_list, self.capture_moves)
            if obstructed:
                break
        
        temp_file = file
        temp_rank = rank

        for i in range(1, 8):
            temp_file, temp_rank = temp_file + 1, temp_rank - 1
            if temp_file > 104 or temp_rank < 1:
                break
            right_down_coord = f"{chr(temp_file)}{temp_rank}"
            obstructed = add_move(current_square, right_down_coord, moves_list, self.capture_moves)
            if obstructed:
                break

        self.moves["moves"] = moves_list
        print(moves_list)
        if self.capture_moves:
            self.moves["capture"] = self.capture_moves

        return self.moves

def add_move(current_square: str, move: str, move_list: list, capture_moves: list) -> bool:
    obstructed = False
    if not square_contains_piece(move):
        move_list.append(move)
    else:
        if not friendly_piece(current_square, move):
            capture_moves.append(move)
            obstructed = True
        else:
            obstructed = True
    return obstructed

# Piece class dictionary
PIECE_CLASS_DICT = {
    "pawn": Pawn,
    "rook": Rook,
    "bishop": Bishop
}