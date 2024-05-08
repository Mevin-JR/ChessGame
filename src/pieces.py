import pygame

king = pygame.image.load('./assets/chess_pieces/b_king_png_shadow_128px.png').convert_alpha()

class Pieces(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.king = king
        self.rect = self.king.get_rect(center=pos)