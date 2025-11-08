from src.models.Player import Player
from src.models.Asteroid import Asteroid
from src.config import *
import pygame
import sys
import random
import math 

def desenhar_texto(surface, text, font, x, y, color=BRANCO):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def start_asteroid_field(asteroides, all_sprites):
    NUM_ASTEROIDES_INICIAIS = 4 
    for _ in range(NUM_ASTEROIDES_INICIAIS):
        # O construtor sem x, y gera o asteroide fora da tela
        ast = Asteroid(size=random.choice([2, 3])) # Começa com Médio e Grande
        asteroides.add(ast)
        all_sprites.add(ast)

def main():
    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO)

    # Taxa de Quadros (FPS)
    clock = pygame.time.Clock()

    try:
        fonte_placar = pygame.font.Font(None, 24) 
    except:
        fonte_placar = pygame.font.SysFont("monospace", 24)

    # Grupo de Sprites
    jogador = Player(LARGURA_TELA // 2, ALTURA_TELA // 2)
    balas = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jogador)

    start_asteroid_field(asteroides, all_sprites)

    # Loop Principal do Jogo
    running = True
    spawn_timer = 0
    while running:
        # Processando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projetil = jogador.atirar()
                    balas.add(projetil)
                    all_sprites.add(projetil)
        
        # Spawn de Asteroides, limitado a 10 na tela
        # Como o FPS é 60, spawn_timer == 120 significa um spawn a cada 2 segundos
        if len(asteroides) < 10 and spawn_timer == 120:
            # choices = 10
            # 1s = 5 => 50%
            # 2s = 3 => 30%
            # 3s = 2 => 20%
            novo_asteroide = Asteroid(random.choice([1, 1, 1, 1, 1, 2, 2, 2, 3, 3]))
            asteroides.add(novo_asteroide)
            all_sprites.add(novo_asteroide)
        
        teclas = pygame.key.get_pressed()
        jogador.handle_input(teclas)

        # Atualização (movimentação, lógica do jogo e tals)
        all_sprites.update()

        # Renderização
        tela.fill(PRETO)
        all_sprites.draw(tela)

        texto_angulo = f"Ângulo: {int((jogador.angle + 90) % 360)}°"
        
        # Desenha o texto no canto superior esquerdo (ex: 10, 10)
        desenhar_texto(tela, texto_angulo, fonte_placar, 10, 10)

        # Atualiza a Tela
        pygame.display.flip()

        # Controla o FPS
        clock.tick(FPS)

        spawn_timer += 1
        spawn_timer %= 121

    pygame.quit()

if __name__ == "__main__":
    main()