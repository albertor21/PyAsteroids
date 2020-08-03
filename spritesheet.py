import pygame
from pygame.locals import *
import math
import os, sys

class SpriteSheet:
    '''
    image : name of the sprite sheet image object
    speed : framerate ( if 0 display current frame)
    frame : frame to be display
    once: display anim once
    '''

    #def __init__(self, filename, speed, cols, rows, once, velRot = 0, frame = 0):
    def __init__(self, image, speed, cols, rows, once, velRot = 0, frame = 0, onlyRow = -1):
        #pygame.sprite.Sprite.__init__(self)
        #self.image = self.load_image(filename, True)
        self.image = image
        self.rect = self.image.get_rect()      
        self.speed = speed
        self.cols = cols #number of cols
        self.rows = rows #number of rows
        self.frames = cols * rows #number of frames
        self.once = once #animate once
        self.done = False #animation done (if once)
        self.frameW = int(self.rect.width / cols)
        self.frameH = int (self.rect.height / rows)
        self.centerX = int(self.frameW / 2)
        self.centerY = int (self.frameH / 2)
        self.frame = frame #current frame (zero-based)
        self.onlyRow = onlyRow
        if self.onlyRow > -1:
            self.setFrame (0, onlyRow) #select 1st col of onlyRow
            self.lastFrame = cols-1 + (row * self.cols)
            self.lastFrame = row * self.cols
        else:
            self.lastFrame = self.frames
            self.firstFrame = 0
        
        self.frameTemp = frame #(float) use to increase frame number according to speed
        self.frameImage = pygame.Surface ((self.frameW, self.frameH), flags=SRCALPHA) #current image frame
        self.angle = 0
        #se hace una mascara con el frame 0 del spritesheet
        rect_frame = (0 , 0, self.frameW, self.frameH)
        self.frameImage.fill ((0,0,0,0))
        self.frameImage.blit (self.image, (0,0), rect_frame) 
        self.mask = pygame.mask.from_surface(self.frameImage)
        self.velRot = velRot
        self.pos = [0,0]
        self.vel = [0,0]
        self.acc = [0,0]

    #col and row are zero-based
    def setFrame(self, col, row):
        if col+1 > self.cols or row + 1 > self.rows:
            raise Exception("col or row exceed max cols or rows")
        #col and row are zero-based
        self.frame = col + (row * self.cols)
    
    def setFrame(self, frame):
        #frame is zero-based
        if frame > self.frames - 1:
            raise Exception("frame exceed max frames")
        self.frame = frame
        
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
        # draw rectangle around the image (DEBUG)
        #pygame.draw.rect (screen, (255, 0, 0), (*origin, *rotated_image.get_size()),1)

    def render(self, screen):
        if not self.done:
            x_rect = (self.frame % self.cols) * self.frameW 
            y_rect = (self.frame // (self.cols)) * self.frameH
            rect_frame = (x_rect , y_rect , self.frameW, self.frameH)
            self.frameImage.fill ((0,0,0,0))
            self.frameImage.blit (self.image, (0,0), rect_frame) 
            #if self.angle == 0: screen.blit (self.frameImage, self.pos)
            #else:
            cRenderImage = self.frameImage.copy()  
            centerSprite =  (self.frameW//2,  self.frameH//2 )
            posRender = (self.pos[0] + centerSprite[0], self.pos[1]+ centerSprite[1] )    
            self.blitRotate(screen, cRenderImage, posRender, centerSprite, self.angle)
               
    def update(self):  
        #update current frame 
        if self.speed > 0:
            self.frameTemp = self.frameTemp + self.speed
            if (self.once and self.frameTemp >= self.lastFrame):
                self.done = True
            if self.frameTemp > self.lastFrame: self.frame = firstFrame
            self.frame = round(self.frameTemp)
        #update rotation velocity
        if self.velRot != 0:
            self.angle += self.velRot
        #update position according to velocity
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] - self.vel[1]