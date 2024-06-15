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

def linear_movement(current_square: str) -> tuple[list, list]:
    file = ord(current_square[0])
    rank = int(current_square[1])
    moves_list = []
    capture_list = []

    # Vertical (up)
    for rank_up in range(rank + 1, RANK_MAX + 1):
        next_coord = f"{chr(file)}{rank_up}"
        if square_rects_dict.get(next_coord) is None:
            break
        if can_capture(current_square, next_coord):
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
            break
        if square_contains_piece(next_coord):
            break
        moves_list.append(next_coord)
    
    return moves_list, capture_list

def diagonal_movement(current_square: str) -> tuple[list, list]:
    file = ord(current_square[0])
    rank = int(current_square[1])
    moves_list = []
    capture_list = []

    # Right Diagonal (up)
    file_step = 0
    for rank_up in range(rank + 1, RANK_MAX + 1):
        file_step += 1
        next_coord = f"{chr(file + file_step)}{rank_up}"
        if square_rects_dict.get(next_coord) is None:
            break
        if can_capture(current_square, next_coord):
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
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
            capture_list.append(next_coord)
            break
        if square_contains_piece(next_coord):
            break
        moves_list.append(next_coord)
    
    return moves_list, capture_list

# Piece objects
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
        obstructed = False
        moves_list = []

        # Vertical movement
        rank_gap1 = 1 if is_white(self.piece_name) else -1
        next_square_rank = rank + rank_gap1
        if RANK_MIN <= next_square_rank <= RANK_MAX:
            next_square_coord = f"{current_square[0]}{next_square_rank}"
            if not square_contains_piece(next_square_coord):
                moves_list.append(next_square_coord)
            else:
                obstructed = True

        if not has_moved(self.piece_name, current_square):
            rank_gap2 = 2 if is_white(self.piece_name) else -2
            next_square_rank = rank + rank_gap2
            if RANK_MIN <= next_square_rank <= RANK_MAX:
                next_square_coord = f"{current_square[0]}{next_square_rank}"
                
                # Check for obstruction along path
                if not obstructed and not square_contains_piece(next_square_coord):
                    moves_list.append(next_square_coord)
            
        # Possible captures in diagonals
        left_diagonal = f"{chr(file - 1)}{rank + rank_gap1}"
        right_diagonal = f"{chr(file + 1)}{rank + rank_gap1}"

        if can_capture(current_square, left_diagonal):
            self.capture_moves.append(left_diagonal)
        if can_capture(current_square, right_diagonal):
            self.capture_moves.append(right_diagonal)  
        
        # Promotion check
        if is_white(self.piece_name) and rank == RANK_MAX - 1 and (moves_list or self.capture_moves):
            self.moves["promotions"] = [f"{chr(file)}{RANK_MAX}"]
        elif not is_white(self.piece_name) and rank == RANK_MIN + 1 and (moves_list or self.capture_moves):
            self.moves["promotions"] = [f"{chr(file)}{RANK_MIN}"]

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves

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
        
        moves_list, self.capture_moves = linear_movement(current_square)
        
        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves

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
        
        moves_list, self.capture_moves = diagonal_movement(current_square)

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves

        return self.moves

class Knight(Piece):

    """
    Calculate and return possible moves for the knight piece

    Move Type:
        - L shaped movement (All sides)
    
    Captures: Along its path
    """

    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        file = ord(current_square[0])
        rank = int(current_square[1])
        moves_list = []

        # Possible knight movement
        directions = {
            "forward_left": (file - 1, rank + 2),
            "forward_right": (file + 1, rank + 2),
            "right_up": (file + 2, rank + 1),
            "right_down": (file + 2, rank - 1),
            "downward_left": (file - 1, rank - 2),
            "downward_right": (file + 1, rank - 2),
            "left_up": (file - 2, rank + 1),
            "left_down": (file - 2, rank - 1),
        }

        for (df, dr) in directions.values():
            if ASCII_A <= df <= ASCII_H and RANK_MIN <= dr <= RANK_MAX:
                next_coord = f"{chr(df)}{dr}"
                if square_rects_dict.get(next_coord) is None:
                    continue
                if can_capture(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                else:
                    if square_contains_piece(next_coord):
                        continue
                    moves_list.append(next_coord)

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves

        return self.moves

class Queen(Piece):

    """
    Calculate and return possible moves for the queen piece

    Move Type:
        - Linear (Vertical & Horizontal)
        - Diagonal (All sides)
    
    Captures: Along its path
    """
    
    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]

        linear_moves, linear_captures = linear_movement(current_square)
        diagonal_moves, diagonal_captures = diagonal_movement(current_square)

        moves_list = linear_moves + diagonal_moves
        self.capture_moves = linear_captures + diagonal_captures

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves

        return self.moves

class King(Piece):

    """
    Calculate and return possible moves for the king piece

    Move Type:
        - One square (In all direction)
    
    Captures: Along its path
    """

    def get_allowed_moves(self) -> dict:
        current_square = get_square(self.current_pos)[0]
        file = ord(current_square[0])
        rank = int(current_square[1])
        moves_list = []

        # Possible king movement
        directions = {
        "left_up": (file - 1, rank + 1),
        "left": (file - 1, rank),
        "left_down": (file - 1, rank - 1),
        "up": (file, rank + 1),
        "down": (file, rank - 1),
        "right_up": (file + 1, rank + 1),
        "right": (file + 1, rank),
        "right_down": (file + 1, rank - 1)
        }

        for (df, dr) in directions.values():
            if ASCII_A <= df <= ASCII_H and RANK_MIN <= dr <= RANK_MAX:
                next_coord = f"{chr(df)}{dr}"
                if square_rects_dict.get(next_coord) is None:
                    continue
                if can_capture(current_square, next_coord):
                    self.capture_moves.append(next_coord)
                else:
                    if square_contains_piece(next_coord):
                        continue
                    moves_list.append(next_coord)

        if moves_list:
            self.moves["moves"] = moves_list
        if self.capture_moves:
            self.moves["captures"] = self.capture_moves
        
        return self.moves

# Piece class dictionary
PIECE_CLASS_DICT = {
    "pawn": Pawn,
    "rook": Rook,
    "bishop": Bishop,
    "knight": Knight,
    "queen": Queen,
    "king": King
}