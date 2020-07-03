import pygame
from pygame.locals import *
import math
import os, sys

class SpriteSheet:
    '''
    filename : name of the sprite sheet image file
    speed : framerate ( if 0 display current frame)
    frames : number of frames
    frame : frame to be display
    once: display anim once
    done: anim terminated
    '''
    def load_image(self,filename, transparent=False):
        try: 
            filename = os.path.join (sys.path[0], filename)
            image = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:   
            print("Cannot load image: " + filename)
            raise SystemExit(message) 
    
        if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
        return image

    def __init__(self, filename, speed, frames, once, velRot = 0, frame = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.load_image(filename, True)
        self.rect = self.image.get_rect()      
        self.speed = speed
        self.frames = frames #number of frames
        self.once = once
        self.done = False
        self.frameW = int(self.rect.width / frames)
        self.frameH = int (self.rect.height)
        self.frame = frame #current frame (zero-based)
        self.frameImage = pygame.Surface ((self.frameW, self.frameH), flags=SRCALPHA) #current image frame
        self.angle = 0
        self.velRot = velRot
        self.pos = [0,0]
        self.vel = [0,0]
        self.acc = [0,0]


    def setFrame(self, frame):
        self.frame = frame
        self.frameImage = pygame.Surface ((self.frameW, self.frameH), flags=SRCALPHA)
        
    def blitRotate(self, screen, image, pos, originPos, angle):
        #https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        # calcaulate the axis aligned bounding box of the rotated image
        w, h       = image.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        # rotate and blit the image
        screen.blit(rotated_image, origin)
        # draw rectangle around the image
        #pygame.draw.rect (screen, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

    def render(self, screen):
        if not self.done:
            rect_frame = (self.frame * self.frameW , 0, self.frameW, self.frameH)
            self.frameImage.fill ((0,0,0,0))
            self.frameImage.blit (self.image, (0,0), rect_frame) 
            if self.angle == 0:    
                screen.blit (self.frameImage, self.pos)
            else:
                cRenderImage = self.frameImage.copy()  
                centerSprite =  (self.frameW//2,  self.frameH//2 )
                posRender = (self.pos[0] + centerSprite[0], self.pos[1]+ centerSprite[1] )    
                self.blitRotate(screen, cRenderImage, posRender, centerSprite, self.angle)
               
    def update(self):  
        if self.speed > 0:
            _frame = self.frame
            _frame = _frame  + math.floor(self.speed )
            if (self.once and _frame >= self.frames):
                self.done = True;
            _frame = _frame % self.frames
            self.frame = _frame
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] - self.vel[1]