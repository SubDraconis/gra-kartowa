import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
tlo = pygame.image.load('tlo.png')
tlo=pygame.transform.scale(tlo, (800, 600))
window.blit(tlo, (0, 0))
pygame.display.update()
run= True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False