import pygame
import os

from utils import *
import UI
import logic

# Initialize pygame
pygame.init()
screenInfo = pygame.display.Info()

# Constants
WIDTH, HEIGHT = screenInfo.current_w - 200, screenInfo.current_h - 100

# Window customizations
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "chess-icon.png")))

# Initialize instances
ui = UI.UI()

chess_board, square_rects = ui.chess_board()
all_pieces = ui.initialize_pieces()

# Variable initialization
selected_piece: UI.Pieces = None
selected_piece_name: str = None
played_moves = []

def show_allowed_moves() -> None: # Highlights allowed moves (by piece)
    move_highlight_color = (90, 90, 90)
    moves_dict, capture_dict = logic.get_allowed_moves(selected_piece_name)
    move_values = [value for value in moves_dict.values() if value is not None] # Available moves
    capture_values = [value for value in capture_dict.values() if value is not None] # Available captures
    
    if len(move_values) == 0:
        return                      # No moves available
    for items in move_values:
        for square in items:
            pygame.draw.circle(WINDOW, move_highlight_color, square.center, 10) # Highlight available moves
    
    if len(capture_values) == 0:
        return                      # No captures available
    for items in capture_values:
        for square in items:
            highlight_square = square.inflate(2, 2)
            pygame.draw.rect(WINDOW, (200, 0, 0), highlight_square, 3) # Highlight available captures

def select_piece() -> None: # Highlight selection of piece
    if selected_piece is not None:
        piece_rect: pygame.Rect = selected_piece.get_rect()
        square_rect = get_square(piece_rect.center)[1]

        overlay_color = (255, 255, 0)
        overlay_surface = pygame.Surface((square_rect.width, square_rect.height), pygame.SRCALPHA)
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
        text_y += 10

def add_graphics() -> None: # Graphics section (board and more...)
    WINDOW.fill(GRAY)
    WINDOW.blit(chess_board, (BOARD_OFFSET_X, BOARD_OFFSET_Y)) # Loading chess board

    select_piece() # Piece selection
    display_moves() # Highlight moves and captures

    all_pieces.update() # Update pieces on board
    all_pieces.draw(WINDOW)
    pygame.display.update() # Display update

def main(): # Main function/loop
    # Variable initialization
    global selected_piece, selected_piece_name
    clicked = False
    selected = False

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
                clicked_square = get_square(mouse_pos)[0]
                if selected and clicked_square is not None: # Piece selected and clicked in valid square
                    friedly_piece = friendly_piece(piece_name, get_piece(mouse_pos)[1])
                    if friedly_piece:
                        selected, piece_name = logic.get_piece(mouse_pos) # Switch selection if clicked on friendly piece
                        selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection
                    else:
                        move = logic.move_piece(piece_name, mouse_pos) # Move piece
                        played_moves.append(move) # Record move
                        selected = False
                        selected_piece = None
                else:
                    selected, piece_name = get_piece(mouse_pos) # Select piece
                    selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection

            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                print("Clicked square: ", get_square(mouse_pos)[0]) # DEBUG

        add_graphics()

    pygame.quit()

if __name__ == "__main__":
    main()