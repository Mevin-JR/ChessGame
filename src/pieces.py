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
    
# Constants
ASCII_A = ord('a')
ASCII_H = ord('h')
RANK_MIN = 1
RANK_MAX = 8

# Helper functions
def can_capture(current_square: str, check_square: str) -> bool:
    if square_rects_dict.get(check_square) is None:
        return False
    if not square_contains_piece(check_square):
        return False
    if friendly_piece(current_square, check_square):
        return False
    return True


class Pawn(Piece):

    """
    Calculate and return possible moves for the pawn piece

    Move Type:
        - 2 squares forward (if pawn not moved)
        - 1 square forward
    
    Captures:
        - Left forward diagonal (1 square)
        - Right forward diagonal (1 square)
    """

    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        file = ord(current_square[0])
        rank = int(current_square[1])
        rank_gap = 1 if is_white(self.piece_name) else -1
        moves_list = []

        # Vertical movement
        if has_moved(self.piece_name, current_square):
            next_square_rank = rank + rank_gap
            if RANK_MIN <= next_square_rank <= RANK_MAX:
                next_square_coord = f"{current_square[0]}{next_square_rank}"
                if not square_contains_piece(next_square_coord):
                    moves_list.append(next_square_coord)
        else:
            start_rank_gap = rank_gap

            for i in range(2):
                next_square_rank = rank + start_rank_gap
                if RANK_MIN <= next_square_rank <= RANK_MAX:
                    next_square_coord = f"{current_square[0]}{next_square_rank}"
                    
                    # If pawn is obstructed stop looking for next square 
                    if i == 0 and square_contains_piece(next_square_coord):
                        break

                    if not square_contains_piece(next_square_coord):
                        moves_list.append(next_square_coord)
                
                    start_rank_gap = start_rank_gap + rank_gap

        # Possible captures in diagonals
        left_diagonal = f"{chr(file - 1)}{rank + rank_gap}"
        right_diagonal = f"{chr(file + 1)}{rank + rank_gap}"

        if can_capture(current_square, left_diagonal):
            self.capture_moves.append(left_diagonal)
        if can_capture(current_square, right_diagonal):
            self.capture_moves.append(right_diagonal)  
        
        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["capture"] = self.capture_moves
        
        return self.moves

class Rook(Piece):

    """
    Calculate and return possible moves for the rook piece

    Move Type:
        - Vertical (Linear)
        - Horizontal (Linear)

    Captures: Along its path
    """

    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        file = ord(current_square[0])
        rank = int(current_square[1])
        moves_list = []

        # Vertical (up)
        for rank_up in range(rank + 1, RANK_MAX + 1):
            next_coord = f"{chr(file)}{rank_up}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)
        
        # Vertical (down)
        for rank_down in range(rank - 1, RANK_MIN - 1, -1):
            next_coord = f"{chr(file)}{rank_down}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)
        
        # Horizontal (right)
        for file_right in range(file + 1, ASCII_H + 1, 1):
            next_coord = f"{chr(file_right)}{rank}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)
        
        # Horizontal (left)
        for file_left in range(file - 1, ASCII_A - 1, -1):
            next_coord = f"{chr(file_left)}{rank}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)
        
        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["capture"] = self.capture_moves

        return self.moves
    
class Bishop(Piece):

    """
    Calculate and return possible moves for the bishop piece

    Move Type:
        - Diagonal (All sides)
    
    Captures: Along its path
    """

    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        file = ord(current_square[0])
        rank = int(current_square[1])
        moves_list = []

        # Right Diagonal (up)
        file_step = 0
        for rank_up in range(rank + 1, RANK_MAX + 1):
            file_step += 1
            next_coord = f"{chr(file + file_step)}{rank_up}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)

        # Right Diagonal (down)
        file_step = 0
        for rank_down in range(rank - 1, RANK_MIN - 1, -1):
            file_step += 1
            next_coord = f"{chr(file + file_step)}{rank_down}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)
        
        # Left Diagonal (up)
        file_step = 0
        for rank_up in range(rank + 1, RANK_MAX + 1):
            file_step -= 1
            next_coord = f"{chr(file + file_step)}{rank_up}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)

        # Left Diagonal (down)
        file_step = 0
        for rank_down in range(rank - 1, RANK_MIN - 1, -1):
            file_step -= 1
            next_coord = f"{chr(file + file_step)}{rank_down}"
            if square_rects_dict.get(next_coord) is None:
                break
            if can_capture(current_square, next_coord):
                self.capture_moves.append(next_coord)
                break
            if square_contains_piece(next_coord):
                break
            moves_list.append(next_coord)

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["capture"] = self.capture_moves

        return self.moves

# Piece class dictionary
PIECE_CLASS_DICT = {
    "pawn": Pawn,
    "rook": Rook,
    "bishop": Bishop,
}