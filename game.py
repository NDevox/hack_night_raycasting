import pygame
import math
from polywog import Polywog

def which_side(x, y):

    pos = {}
    pos['zero_x'] = False

    if x < 0:
        pos['left'] = False
    elif x > 0:
        pos['left'] = True
    else:
        pos['left'] = False
        pos['zero_x'] = True

    pos['zero_y'] = False

    if y < 0:
        pos['bottom'] = False
    elif y > 0:
        pos['bottom'] = False
    else:
        pos['bottom'] = False
        pos['zero_y'] = True

    return pos


def workout_angles(person, shape):
    angles = []
    for point in shape:
        x, y = person[0] - point[0], person[1] - point[1]
        pos = which_side(x, y)

        if (pos['left'] and not pos['bottom']) \
            or not pos['left'] and pos['bottom']:
            angles.append((point, math.atan(y/x), pos))

        else:
            angles.append((point, math.atan(x/y), pos))

    angles.sort(key=lambda x: x[1])

    return angles[0], angles[-1]


def create_polygon(person, shape, size=(0,0)):
    angles = workout_angles(person, shape)

    points = []

    for angle in angles:
        if angle[2]['left'] and not angle[2]['bottom']:
            points.append((round(person[1] - (person[0] * math.tan(angle[1]))), size[1]))

        elif not angle[2]['left'] and not angle[2]['bottom']:
            points.append((round(person[0] - ((size[1] - person[1]) * math.tan(angle[1]))), 0))

        elif not angle[2]['left'] and angle[2]['bottom']:
            points.append((0, person[1]  + round((person[0] * math.tan(angle[1])))))

        elif angle[2]['left'] and angle[2]['bottom']:
            points.append((0, person[1]  + round((person[0] * math.tan(angle[1])))))

    return points + [angles[0][0], angles[1][0]]


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

        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[1][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[1][0], player.rect.center], 1)
        pygame.draw.polygon(screen, color, create_polygon(player.rect.center, block.corners(), (800, 640)), 1)
        pygame.draw.polygon(screen, color, create_polygon(player.rect.center, block2.corners(), (800, 640)), 1)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
