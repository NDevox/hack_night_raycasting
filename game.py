import pygame
import math
from polywog import Polywog


def which_side(x, y):
    """
    We need to figure out which quadrant the polygon is in relative to our point.
    :param x: int, x co-ord difference
    :param y: int, y co-ord difference
    :return: dict, containing if the polygon is left and below the point.
    """
    pos = {}

    if x < 0:  # it is not left
        pos['left'] = False
    elif x > 0:
        pos['left'] = True
    else:  # I believe a false here avoids a DivisionByZero error.
        pos['left'] = False

    if y < 0:  # it is not below
        pos['bottom'] = False
    elif y > 0:
        pos['bottom'] = False
    else:  # avoiding DivisionByZero
        pos['bottom'] = False

    return pos


def workout_angles(person, shape):
    """
    Find the angles with the largest difference on all the triangles between the shapes vertices and the person.

    :param person: tuple (x,y), the persons co-ordinates
    :param shape: list[tuple(x,y)], list of the vertices co-ordinates for a shape
    :return: list[tuple((x,y), (angle))], list of tuples holding the co-ordinates in a tuple, and the angle.
    """
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


def create_polygon(person, shape, size=(0, 0)):
    """
    Using the person position and shape, calculate a polygon for its shadow.

    :param person: tuple(x,y), the persons co-ordinates.
    :param shape: list[tuple(x,y)], a list of a shapes vertices.
    :param size: tuple(x,y), the size of the screen.
    :return: list[tuple(x,y)], a list of co-ordinates for the shadow to be drawn.
    """
    angles = workout_angles(person, shape)  # Lets get the angles to find the points on the wall.

    points = []

    # I think we all now know that I am not good at trig under pressure.
    for angle in angles:
        if angle[2]['left'] and not angle[2]['bottom']:
            points.append((person[1] - round(person[0] * math.tan(angle[1])), 0))

        elif not angle[2]['left'] and not angle[2]['bottom']:
            points.append((person[0] - round((size[1] - person[1]) * math.tan(angle[1])), 0))

        elif not angle[2]['left'] and angle[2]['bottom']:
            points.append((size[0], person[0] - round((size[1] - person[1]) * math.tan(angle[1]))))

        elif angle[2]['left'] and angle[2]['bottom']:
            points.append((size[0], person[1] - round((person[0] * math.tan(angle[1])))))

    # I'll think of why this logically works soon.
    return sorted(points + [angles[0][0], angles[1][0]], key=lambda x:min(map(abs, x)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    done = False
    x = 400
    y = 320
    color = (200, 200, 255)
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
        pygame.draw.polygon(screen, color, create_polygon(player.rect.center, block.corners(), (800, 640)), 0)
        pygame.draw.polygon(screen, color, create_polygon(player.rect.center, block2.corners(), (800, 640)), 0)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
