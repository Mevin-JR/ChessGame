import pygame
import UI
import logic

# Initialize pygame
pygame.init()
screenInfo = pygame.display.Info()

FONT32 = pygame.font.Font(None, 32)
WIDTH, HEIGHT = screenInfo.current_w - 100, screenInfo.current_h - 100
FPS = 60

# Window customizations
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
pygame.display.set_icon(pygame.image.load("./assets/chess-icon.png"))

# Initialize chess board & pieces
board_offset_x, board_offset_y = 100, 50
chess_board, square_rects = UI.chess_board(FONT32, board_offset_x, board_offset_y)
black, white, all_pieces = UI.initialize_pieces()

def add_graphics() -> None:
    WINDOW.fill((50,50,50))
    WINDOW.blit(chess_board, (board_offset_x, board_offset_y))
    # for square_rect in square_rects.values():
    #     border_rect = square_rect.inflate(2, 2)
    #     pygame.draw.rect(WINDOW, (255, 255, 255), border_rect, 1)
    
    # Chess pieces
    all_pieces.update()
    all_pieces.draw(WINDOW)

    pygame.display.update()

def main():
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
                if selected is True and logic.get_square(mouse_pos) is not None:
                    if logic.own_piece(piece_name, logic.get_piece(mouse_pos)[1]):
                        selected, piece_name = logic.get_piece(mouse_pos)
                    else:
                        logic.move_piece(piece_name, mouse_pos)
                        selected = False
                else:
                    selected, piece_name = logic.get_piece(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                print("Clicked: ", logic.get_square(mouse_pos)) # DEBUG

        add_graphics()

    pygame.quit()

if __name__ == "__main__":
    main()