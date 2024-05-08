import pygame
import os

# Initialize pygame
pygame.init()
font = pygame.font.Font(None, 32)
screenInfo = pygame.display.Info()

# Initialize var
piece_dir = "./assets/chess_pieces"
files = os.listdir(piece_dir)

# Chess board UI
def chess_board(pygame):

    # Board background
    sq_dark = (184,139,74)
    sq_light = (227,193,111)
    square_size = 80

    for row in range(8):
        for col in range(8):
            color = sq_light if (row + col) % 2 == 0 else sq_dark
            pygame.draw.rect(background, color, pygame.Rect(250 + col * square_size, 50 + row * square_size, square_size, square_size))
    
    # Chess notations
    x_alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    alph_count = 0
    x_left_init = 285
    x_top = 715

    y_num = 8
    y_left = 200
    y_top_init = 80

    for row in range(9):
        if row < 8:
            y_label = font.render(str(y_num), True, (255, 255, 255))
            background.blit(y_label, (y_left, y_top_init))
            y_num -= 1
            y_top_init = 80 + (row + 1) * square_size
        else:
            for col in range(8):
                x_label = font.render(x_alph[alph_count], True, (255, 255, 255))
                background.blit(x_label, (x_left_init, x_top))
                alph_count += 1
                x_left_init = 285 + (col + 1) * square_size

# Chess pieces
def get_black_pieces():
    b_pieces = [piece_dir + "/" + png for png in files if "b_" in png]
    return b_pieces

def get_white_pieces():
    w_pieces = [png for png in files if "w_" in png]
    return w_pieces


# GUI customizations
w,h = screenInfo.current_w -100, screenInfo.current_h - 100
background = pygame.display.set_mode([w,h], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
icon = pygame.image.load("./assets/chess-icon.png")
pygame.display.set_icon(icon)

def initialize_pieces(pygame):
    for piece in get_black_pieces():
        b_piece_raw = pygame.image.load(str(piece)).convert_alpha()
        yield b_piece_raw                                                   # TODO: Complete this part & below

class Pieces(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

black_pieces_list = list(initialize_pieces(pygame))
black_pieces = [Pieces(image, (x,y)) for image, (x,y) in zip(black_pieces_list, [(100, 100), (200,200), (300, 300), (400, 400)])]

black = pygame.sprite.Group()
black.add(piece for piece in black_pieces)

running = True
clock = pygame.time.Clock()
while running:
    background.fill((50,50,50))
    chess_board(pygame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #black.update()
    #black.draw(background)
    pygame.display.update()
    clock.tick(60)
pygame.quit()