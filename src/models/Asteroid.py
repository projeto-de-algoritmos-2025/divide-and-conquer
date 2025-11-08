import pygame
import random
import math
from src.config import *

class Asteroid(pygame.sprite.Sprite):
    # Mapeamento do número (tamanho) aos atributos de nível
    TAMANHOS = {
        3: {"nivel": "Grande", "raio": 120, "velocidade_max": 1}, # asteroid3.png
        2: {"nivel": "Medio", "raio": 60, "velocidade_max": 2}, # asteroid2.png
        1: {"nivel": "Pequeno", "raio": 20, "velocidade_max": 3} # asteroid1.png
    }

    def __init__(self, size:int):
        super().__init__()
        
        # Definindo atributos com base no tamanho
        self.size = size
        props = self.TAMANHOS.get(size, self.TAMANHOS[3]) 
        self.nivel = props["nivel"]
        self.raio = props["raio"]
        self.velocidade_max = props["velocidade_max"]

        # gerando posição inicial fora da tela
        self.x, self.y = self._generate_initial_coordinates()

        # gerando velocidade inicial
        self.vx, self.vy = self._generate_initial_velocity()

        # Angulação inicial e velocidade de rotação do asteroide
        self.angle = random.uniform(0, 360) 
        self.rot_speed = random.uniform(-1, 1) # Velocidade de rotação visual
        
        # Escolhendo a imagem do asteroide
        self.original_image = pygame.image.load(f"src/assets/asteroid{size}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.raio, self.raio))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
    
    def _generate_initial_velocity(self):
        angle_rad = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(0.5, self.velocidade_max) 
        
        vx = velocidade * math.cos(angle_rad)
        vy = velocidade * math.sin(angle_rad)
        return vx, vy

    def _generate_initial_coordinates(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        # A posição inicial é calculado pra fora da borda, para garantir que 
        # o asteroide inteiro comece fora e entre na tela gradualmente.
        if side == 'top':
            # y = 0 - tamanho do asteroide
            # x varia entre 0 e LARGURA_TELA
            x = random.randint(0, LARGURA_TELA)
            y = -self.raio 
        elif side == 'bottom':
            # y = ALTURA_TELA + tamanho do asteroide
            # x varia entre 0 e LARGURA_TELA
            x = random.randint(0, LARGURA_TELA)
            y = ALTURA_TELA + self.raio
        elif side == 'left':
            # x = 0 - tamanho do asteroide
            # y varia entre 0 e ALTURA_TELA
            x = -self.raio
            y = random.randint(0, ALTURA_TELA)
        else: # 'right'
            # x = LARGURA_TELA + tamanho do asteroide
            # y varia entre 0 e ALTURA_TELA
            x = LARGURA_TELA + self.raio
            y = random.randint(0, ALTURA_TELA)

        return float(x), float(y)
    
    def update(self):
        # Atualiza a Posição (Movimento)
        self.x += self.vx
        self.y += self.vy

        # Teletransporte nas bordas da tela
        # O asteroide desaparece quando o centro dele passa mais de um raio para fora da tela.
        # Ele reaparece no lado oposto com a mesma distância para dentro.
        if self.x > LARGURA_TELA + self.raio:
            self.x = -self.raio
        elif self.x < -self.raio:
            self.x = LARGURA_TELA + self.raio
            
        if self.y > ALTURA_TELA + self.raio:
            self.y = -self.raio
        elif self.y < -self.raio:
            self.y = ALTURA_TELA + self.raio
        
        # Atualiza a rotação, dentro entre 0 e 360 graus
        self.angle += self.rot_speed
        self.angle %= 360
        
        # Atualiza a imagem rotacionada e o retângulo de colisão
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))