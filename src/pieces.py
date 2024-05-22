from utils import *

class Pawn:
    def __init__(self, pawn_name: str, current_pos: tuple, dest_pos: tuple = None):
        self.pawn_name = pawn_name
        self.current_pos = current_pos
        self.dest_pos = dest_pos
        self.moves = {}

    def get_allowed_moves(self) -> tuple[bool, dict]:
        can_move = True
        current_square = get_square(self.current_pos)[0]
        dest_square = get_square(self.dest_pos)[0] if self.dest_pos is not None else None

        starting_rank = int(current_square[1])
        direction = 1 if is_white(self.pawn_name) else -1

        if has_moved(self.pawn_name, current_square):
            next_square_rank = starting_rank + direction
            next_square_coord = f"{current_square[0]}{next_square_rank}"

            if square_rects_dict.get(next_square_coord) is not None and not square_contains_piece(next_square_coord):
                self.moves["forward"] = [next_square_coord]

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
                
                direction_2 = direction_2 + 1 if is_white(self.pawn_name) else direction_2 - 1

            if forward_moves:
                self.moves["forward"] = forward_moves
            else:
                can_move = False

        capture_moves = self.get_capture_moves(current_square, direction)
        if capture_moves:
            self.moves["capture"] = [move for move in capture_moves]
        
        if dest_square is not None:
            for move_list in self.moves.values():
                if dest_square in move_list:
                    can_move = True
        
        return can_move, self.moves

    def get_capture_moves(self, current_square: str, direction: int) -> list:
        capture_moves = []
        left_diagonal = f"{chr(ord(current_square[0]) - 1)}{int(current_square[1]) + direction}"
        right_diagonal = f"{chr(ord(current_square[0]) + 1)}{int(current_square[1]) + direction}"

        if square_rects_dict.get(left_diagonal) is not None and square_contains_piece(left_diagonal) and not friendly_piece(current_square, left_diagonal):
            capture_moves.append(left_diagonal)
        if square_rects_dict.get(right_diagonal) is not None and square_contains_piece(right_diagonal) and not friendly_piece(current_square, right_diagonal):
            capture_moves.append(right_diagonal)    
            
        return capture_moves
