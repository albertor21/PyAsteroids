import pygame
from pygame.locals import *
 

class Ship(pygame.sprite.Sprite):
    def __init__(self, filename, speed, frames, once, index, frame, done = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = (0,0)
        self.speed = [0.5, -0.5]
        self.frames = frames
        self.once = once
        self.done = done
        self.index = index
        self.frame = frame
    #añadido para dibujar un solo frame a eleccion con el metodo setFrame(frame)
    
    def update(self):
        pass
        
    def render(self, rectangle):
        rect = pygame.Rect(rectangle)
        result_image = pygame.Surface(rect.size).convert_alpha()
        result_image.blit(self.image, (0, 0), rect)
        return result_image