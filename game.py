import pygame
import math
from polywog import Polywog

def workout_angles(person, shape):
    angles = []
    for point in shape:
        x, y = person[0] - point[0], person[1] - point[1]
        angles.append((point, math.atan(x/y)))

    angles.sort(key=lambda x: x[1])

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



        player.rect.x = x
        player.rect.y = y
        block = Polywog(color)
        block.rect.x = 600
        block.rect.y = 200
        block_list.add(block)

        block2 = Polywog(color)
        block2.rect.x = 100
        block2.rect.y = 100
        block_list.add(block2)
        block_list.draw(screen)

        #print(block.corners())
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[1][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[1][0], player.rect.center], 1)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
