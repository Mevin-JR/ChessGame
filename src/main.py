import pygame
import os

import UI
import logic

# Initialize pygame
pygame.init()
screenInfo = pygame.display.Info()

FONT32 = pygame.font.Font(None, 32)
WIDTH, HEIGHT = screenInfo.current_w - 100, screenInfo.current_h - 100
BOARD_OFFSET_X, BOARD_OFFSET_Y = 100, 50
FPS = 60

# Window customizations
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "chess-icon.png")))

# Initialize chess board & pieces
chess_board, square_rects = UI.chess_board(FONT32, BOARD_OFFSET_X, BOARD_OFFSET_Y)
black, white, all_pieces = UI.initialize_pieces()

selected_piece: UI.Pieces = None

def select_piece() -> None:
    if selected_piece is not None:
        piece_rect: pygame.Rect = selected_piece.get_rect()
        square_rect = logic.get_square(piece_rect.center)[1]

        overlay_color = (255, 255, 0)
        overlay_surface = pygame.Surface((square_rect.width, square_rect.height), pygame.SRCALPHA)
        overlay_surface.fill(overlay_color)
        overlay_surface.set_alpha(70)

        WINDOW.blit(overlay_surface, square_rect.topleft)

def add_graphics() -> None:
    WINDOW.fill((50,50,50))
    WINDOW.blit(chess_board, (BOARD_OFFSET_X, BOARD_OFFSET_Y)) 

    # Chess pieces
    select_piece()
    all_pieces.update()
    all_pieces.draw(WINDOW)

    pygame.display.update()
    # for square_rect in square_rects.values():
    #     border_rect = square_rect.inflate(2, 2)
    #     pygame.draw.rect(WINDOW, (255, 255, 255), border_rect, 1)

def main():
    global selected_piece

    clock = pygame.time.Clock()
    clicked = False
    selected = False
    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:  # TODO: Recognize mouse drag
                clicked = True
                if selected is True and logic.get_square(mouse_pos)[0] is not None:
                    if logic.own_piece(piece_name, logic.get_piece(mouse_pos)[1]):
                        selected, piece_name = logic.get_piece(mouse_pos)
                        selected_piece = UI.chess_pieces.get(piece_name)
                    else:
                        logic.move_piece(piece_name, mouse_pos)
                        selected = False
                        selected_piece = None
                else:
                    selected, piece_name = logic.get_piece(mouse_pos)
                    selected_piece = UI.chess_pieces.get(piece_name)
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                print("Clicked: ", logic.get_square(mouse_pos)[0]) # DEBUG

        add_graphics()

    pygame.quit()

if __name__ == "__main__":
    main()