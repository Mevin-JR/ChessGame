import pygame
import UI

# Initialize pygame
pygame.init()
font = pygame.font.Font(None, 32)
screenInfo = pygame.display.Info()

# GUI customizations
w,h = screenInfo.current_w - 100, screenInfo.current_h - 100
background = pygame.display.set_mode([w,h], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
icon = pygame.image.load("./assets/chess-icon.png")
pygame.display.set_icon(icon)

board_offset_x, board_offset_y = 100, 50
chess_board, square_rects = UI.chess_board(font, board_offset_x, board_offset_y) # Preloaded chess board
black, white = UI.initialize_pieces()

clicked = False
running = True
clock = pygame.time.Clock()
while running:
    background.fill((50,50,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:  # For drag, store mousebtndown & up
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            print(UI.get_clicked_square(mouse_pos))

    background.blit(chess_board, (board_offset_x, board_offset_y))
    # for square_rect in square_rects.values():
    #     border_rect = square_rect.inflate(2, 2)
    #     pygame.draw.rect(background, (255, 255, 255), border_rect, 1)
    
    black.update()
    black.draw(background)
    white.update()
    white.draw(background)

    pygame.display.update()
    clock.tick(60)
pygame.quit()