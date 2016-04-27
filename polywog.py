import pygame

class Polywog(pygame.sprite.Sprite):

    def __init__(self, color):
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.Surface([50, 50])
       self.image.fill(color)

       self.rect = self.image.get_rect()