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
            angles.append((point, math.atan(y/x)))

        else:
            angles.append((point, math.atan(x/y)))

    angles.sort(key=lambda x: x[1])

    return angles[0], angles[-1]


def create_polygon(person, shape, size=(0,0)):
    angles = workout_angles(person, shape)
    #if shape if left and above point then we go 0 0
    #if shape is right and above point theb we go 1 0
    #if shape is left and down w
    # will do
    # the dude in front had  really good point if it is easy to do in python
    # polar co-ordinates
    first_point = (person[0] - person[1]) * math.sin(angles[0][1])
    second_point = (person[1] - person[0])*math.sin(math.pi/2 - angles[1][1])

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
        print(create_polygon(player.rect.center, block.corners()))
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block.corners())[1][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[0][0], player.rect.center], 1)
        pygame.draw.lines(screen, color, False, [workout_angles(player.rect.center, block2.corners())[1][0], player.rect.center], 1)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
