import pygame

pygame.init()
screen = pygame.display.set_mode((800, 640))
done = False
x = 400
y = 320

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] or pressed[pygame.K_w]: y -= 3
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]: y += 3
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: x -= 3
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]: x += 3

    screen.fill((0, 0, 0))
    color = (255, 100, 0)
    pygame.draw.polygon(screen, color, [[105,105],[205,205],[255,255],[105,255]],1)
    pygame.draw.polygon(screen, color, [[400,400],[500,400],[500,500],[400,500]],1)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 5, 5))

    pygame.display.flip()
    clock.tick(60)