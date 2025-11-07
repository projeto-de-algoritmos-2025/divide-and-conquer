import pygame
from src.config import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int):
        super().__init__()
        self.raio = 15

        # começar nas coordenadas dadas
        self.x = float(x)
        self.y = float(y)

        # velocidade nos eixos
        self.vx = 0.0
        self.vy = 0.0

        # angulo inicial
        self.angle = 0.0
        self.cos_angle = 0
        self.sin_angle = 0

        self.original_image = pygame.image.load("src/assets/asteroid2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.raio*5, self.raio*5))
        self.image = self.original_image
    
    def update(self):
        # rotacionando o player
        self.image = pygame.transform.rotate(self.original_image, self.angle + 1)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
