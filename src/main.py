import pygame
import os

from utils import *
from pieces import *
from UI import *
import logic

# Initialize pygame
pygame.init()
screenInfo = pygame.display.Info()

# Constants
#WIDTH, HEIGHT = screenInfo.current_w - 200, screenInfo.current_h - 100
WIDTH, HEIGHT = 1000, 800 # Temp

# Window customizations
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "chess-icon.png")))


# Variable initialization
selected_piece: pygame.Rect = None
selected_piece_name: str = None
possible_moves = {}
played_moves = []

ui = UI() # Instance initialize
chess_board, square_rects = ui.chess_board()
all_pieces = ui.initialize_pieces()

def show_allowed_moves() -> None: # Highlights allowed moves (by piece)
    if not possible_moves:
        return
    
    moves = possible_moves.get("moves", [])
    captures = possible_moves.get("captures", [])
    promotions = possible_moves.get("promotions", [])
    
    if moves:
        for square in moves:
            if square in promotions:
                continue
            square_rect: pygame.Rect = square_rects_dict.get(square)
            pygame.draw.circle(WINDOW, DARK_GRAY, square_rect.center, 10) # Highlight available moves
    
    if captures:
        capture_highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        capture_highlight_surface.fill(RED)
        capture_highlight_surface.set_alpha(90)
        for capture_square in captures:
            capture_square_rect: pygame.Rect = square_rects_dict.get(capture_square)
            WINDOW.blit(capture_highlight_surface, capture_square_rect.topleft) # Highlight capture moves

    if promotions:
        for square in promotions:
            square_rect: pygame.Rect = square_rects.get(square)
            pygame.draw.line(WINDOW, DARK_GRAY, (square_rect.centerx - 10, square_rect.centery), (square_rect.centerx + 10, square_rect.centery), 5)
            pygame.draw.line(WINDOW, DARK_GRAY, (square_rect.centerx, square_rect.centery - 10), (square_rect.centerx, square_rect.centery + 10), 5)

def piece_highlight() -> None: # Highlight selection of piece
    if selected_piece is not None:
        piece_rect: pygame.Rect = selected_piece
        square_rect = get_square_rect(piece_rect.center)

        overlay_color = (255, 255, 0)
        overlay_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        overlay_surface.fill(overlay_color)
        overlay_surface.set_alpha(70)

        show_allowed_moves()
        WINDOW.blit(overlay_surface, square_rect.topleft)

def display_moves(): # TODO: Fix design
    background_rect = pygame.Rect(WIDTH - 500, 50, 300, 300)
    pygame.draw.rect(WINDOW, (30, 30, 30), background_rect, border_radius = 20)
    text_y = background_rect.top + 10
    for move in played_moves:
        text_surface = FONT32.render(move, True, (255, 255, 255))
        WINDOW.blit(text_surface, (background_rect.left + 10, text_y))
        text_y += 30

def add_graphics() -> None: # Graphics section (board and more...)
    WINDOW.fill(GRAY)
    WINDOW.blit(chess_board, (BOARD_OFFSET_X, BOARD_OFFSET_Y)) # Loading chess board

    piece_highlight() # Piece selection
    #display_moves() # Highlight moves and captures

    all_pieces.update() # Update pieces on board
    all_pieces.draw(WINDOW)
    pygame.display.update() # Display update

def select_piece(piece_name: str, piece_rect: pygame.Rect, mouse_pos: tuple[int, int]) -> None:
    global selected_piece, selected_piece_name, possible_moves
    selected_piece = piece_rect
    selected_piece_name = piece_name
    possible_moves = logic.get_allowed_moves(piece_name, mouse_pos)

def handle_player_interaction(mouse_pos: tuple[int, int]):
    clicked_square = get_square_coord(mouse_pos)
    if clicked_square is None:
        return
    global selected_piece, selected_piece_name
    selected = True if selected_piece is not None else False
    if is_square_occupied(clicked_square):
        piece_name = get_piece_name(clicked_square)
        piece_rect: pygame.Rect = chess_pieces_dict.get(piece_name).get_rect()
        if not selected:
            select_piece(piece_name, piece_rect, mouse_pos)
        else:
            selected_piece_square = get_piece_square(selected_piece_name)
            if is_friendly(get_piece_square(piece_name), selected_piece_square):
                select_piece(piece_name, piece_rect, mouse_pos)
                return
            logic.move_piece(selected_piece_name, mouse_pos)
            selected_piece = None
            selected_piece_name = None
    else:
        if not selected:
            return
        logic.move_piece(selected_piece_name, mouse_pos)
        selected_piece = None
        selected_piece_name = None

# def temp(mouse_pos: tuple[int, int]):
#     global selected_piece, selected_piece_name, allowed_moves
#     previous_turn = 0 # Black - 0, White - 1
#     selected = False
#     clicked_square = get_square_coord(mouse_pos)
#     if selected and clicked_square is not None: # Piece selected and clicked in valid square
#         piece_rect: pygame.Rect = chess_pieces_dict.get(piece_name).get_rect()
#         if is_friendly(piece_rect.center, mouse_pos):
#             piece_name = get_piece_name(mouse_pos) # Switch selection if clicked on friendly piece
#             if piece_name is not None:
#                 #if (previous_turn == 0 and is_white(piece_name)) or (previous_turn == 1 and not is_white(piece_name)): # Check for turn
#                 selected = True
#                 selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection
#                 allowed_moves = logic.get_allowed_moves(piece_name, mouse_pos)
#         else:
#             move = logic.move_piece(piece_name, mouse_pos) # Move piece
#             if move is not None:
#                 played_moves.append(move) # Record move
#                 if is_white(piece_name):
#                     previous_turn = 1
#                 else:
#                     previous_turn = 0                 
#             selected = False
#             selected_piece = None # Reset selection
#     elif clicked_square is not None:
#         piece_name = get_piece_name(mouse_pos) # Switch selection if clicked on friendly piece
#         if piece_name is not None:
#             #if (previous_turn == 0 and is_white(piece_name)) or (previous_turn == 1 and not is_white(piece_name)): # Check for turn
#             selected = True
#             selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection
#             allowed_moves = logic.get_allowed_moves(piece_name, mouse_pos)

def main(): # Main function/loop
    clicked = False
    clock = pygame.time.Clock()
    running = True
    while running: # Main loop
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
                handle_player_interaction(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                print("Clicked square: ", get_square_coord(mouse_pos)) # DEBUG

        add_graphics()

    pygame.quit()

if __name__ == "__main__":
    main()