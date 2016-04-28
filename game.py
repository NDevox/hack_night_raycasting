import pygame
import math
from polywog import Polywog


def get_x_y(pos1, pos2):
    """
    Get the difference between two co-ordinates.

    :param pos1: tuple, co-ordinate 1.
    :param pos2: tuple, co-ordinate 2.
    :return: tuple, co-ordinate difference.
    """
    return pos1[0] - pos2[0], pos1[1] - pos2[1]


def which_side(x, y):
    """
    We need to figure out which quadrant the polygon is in relative to our point.

    :param x: int, x co-ord difference.
    :param y: int, y co-ord difference.
    :return: dict, containing if the polygon is left and below the point.
    """
    pos = {}

    if x < 0:  # it is not left
        pos['left'] = False
    elif x > 0:
        pos['left'] = True
    else:  # I believe a false here avoids a DivisionByZero error.
        pos['left'] = False

    if y < 0:  # it is below
        pos['bottom'] = False
    elif y > 0:
        pos['bottom'] = True
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
        x, y = get_x_y(person, point)
        pos = which_side(x, y)
        try:
            if (pos['left'] and not pos['bottom']) \
                or not pos['left'] and pos['bottom']:
                angles.append((point, math.atan(y/x), pos))

            else:
                angles.append((point, math.atan(x/y), pos))
        except ZeroDivisionError:
            pass

    angles.sort(key=lambda x: x[1])

    return angles[0], angles[-1]


def angle_y(angle, pos, corner):
    """
    Is the angle between the corner to the polygon bigger than the polygon to the person?

    :param angle: float, Angle between person and polygon.
    :param pos: tuple(x,y), Polygon position.
    :param corner: tuple(x,y), corner.
    :return: bool, it is or isn't.
    """
    x, y = get_x_y(pos, corner)

    return math.atan(x/y) > angle


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

    for angle in angles:

        m = (angle[0][1] - person[1])/(angle[0][0]-person[0])
        c = (m*person[0] - person[1])
        # They are in the top left.
        if angle[2]['left'] and not angle[2]['bottom']:
            if angle_y(angle[1], angle[0], (0,0)):
                y = person[1] - round(person[0] * math.tan(angle[1]))
                points.append((0, y))
            else:
                x = person[0] - round(person[1] / math.tan(angle[1]))
                points.append((x, 0))

        # They are in the top right.
        elif not angle[2]['left'] and not angle[2]['bottom']:
            if angle_y(angle[1], angle[0], (size[0],0)):
                print(1)
                y = round(m * size[0] + c)
                points.append((size[0], y))
            else:
                print(2)
                x = round((0 + c) / m)
                points.append((x, 0))

        # They are in the bottom right.
        elif not angle[2]['left'] and angle[2]['bottom']:
            if angle_y(angle[1], angle[0], size):
                y = person[1] + round(person[0] * math.tan(angle[1]))
                points.append((size[0], y))
            else:
                x = person[0] + round(person[1] / math.tan(angle[1]))
                points.append((x, size[1]))

        # They are in the bottom left.
        elif angle[2]['left'] and angle[2]['bottom']:
            if angle_y(angle[1], angle[0], (0,size[1])):
                y = round(m * 0 + c)
                points.append((0, y))
            else:
                x = round((size[1] + c) / m)
                points.append((x, size[1]))

    # I'll think of why this logically works soon.
    return sorted(points + [angles[0][0], angles[1][0]], key=lambda x:max(map(abs, x)))


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

        for obj in block_list:
            # draw lines of sight to the corners.
            pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, obj.corners())[0][0], player.rect.center], 1)
            pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, obj.corners())[1][0], player.rect.center], 1)

            # Draw the shadows.
            pygame.draw.polygon(screen, color, create_polygon(player.rect.center, obj.corners(), (800, 640)), 0)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
