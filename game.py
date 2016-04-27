import pygame
import math
from polywog import Polywog

def workout_angles(person, shape):
    angles = []
    for point in shape:
        x, y = person[0] - point[0], person[1] - point[1]
        angles.append((point, math.atan(x/y)))

    angles.order(key=lambda x: x[1])

    return angles[0], angles[-1]


def create_polygon(person, shape, size=(0,0)):
    angles = workout_angles(person, shape)
    first_point = person[0] - person[1]*math.tan(angles[0])
    second_point = person[1] - person[0]*math.tan(90 - angles[1])

    return first_point, second_point, angles[0][0], angles[1][0]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    done = False
    x = 400
    y = 320
    color = (255, 100, 0)
    player = Polywog(color)
    clock = pygame.time.Clock()
    block_list = pygame.sprite.Group()
    block_list.add(player)
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

        pygame.draw.polygon(screen, color, [[105,105],[205,205],[255,255],[105,255]], 1)

        pygame.draw.polygon(screen, color, [[400,400],[500,400],[500,500],[400,500]], 1)


        player.rect.x = x
        player.rect.y = y
        block = Polywog(color)
        block.rect.x = 600
        block.rect.y = 200
        block_list.add(block)
        block_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
