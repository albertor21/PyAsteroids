
# Módulos
import sys, pygame, os
import math
from pygame.locals import *

 
# Constantes
WIDTH = 800
HEIGHT = 600

 
# Clases
# ---------------------------------------------------------------------
class SpriteSheet(pygame.sprite.Sprite):
    '''
    filename : name of the sprite sheet image file
    speed : framerate ( if 0 display current frame)
    frames : number of frames
    frame : frame to be display
    once: display anim once
    done: anim terminated
    '''
    def __init__(self, filename, speed, frames, once, frame = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(filename, True)
        self.rect = self.image.get_rect()      
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = speed
        self.frames = frames #number of frames
        self.once = once
        self.done = False
        self.frameW = int(self.rect.width /frames)
        self.frameH = int (self.rect.height)
        self.frame = frame #current frame (zero-based)
        self.frameImage = pygame.Surface ((self.frameW, self.frameH), flags=SRCALPHA) #current image frame
        self.angle = 0
        
    def blitRotate(self, surf, image, pos, originPos, angle):
        #https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        # calculate the axis aligned bounding box of the rotated image
        w, h       = image.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2 (originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate (angle)
        pivot_move   = pivot_rotate - pivot
        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        # rotate and blit the image
        #####surf.blit(rotated_image, origin)
        return rotated_image
        # draw rectangle around the image
        #pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)     

    def render(self, screen):
        if not self.done:
            rect_frame = (self.frame * self.frameW , 0, self.frameW, self.frameH)
            if self.angle == 0:
                self.frameImage.fill ((0,0,0,0))
                self.frameImage.blit (self.image, (0,0), rect_frame)
                #self.frameImage.convert_alpha()
            else:
                pass
                #surf.blit (self.image, (0,0), rect_frame)
                self.blitRotate(screen, self.image, (300,300), (40,37), self.angle)
                #self.blitRotate(screen, surf, (300,300), (80,37), self.angle)
        return self.frameImage

    def update(self, dt):  
        if self.speed > 0:
            _frame = self.frame
            _frame = _frame  + math.floor(self.speed )
            if (self.once and _frame >= self.frames):
                self.done = True;
            _frame = _frame % self.frames
            self.frame = _frame
          
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
 
def load_image(filename, transparent=False):
    try: 
        filename = os.path.join (sys.path[0], filename)
        image = pygame.image.load(filename).convert_alpha()
        #image = pygame.image.load(filename).convert()
    except pygame.error as message:   
        print("Cannot load image: " + filename)
        raise SystemExit(message) 
    
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def texto(texto, posx, posy,  size, color=(255, 255, 255)):
    fontfile = os.path.join (sys.path[0], 'fonts/ledger-Regular.ttf')
    fuente = pygame.font.Font(fontfile, size)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyAsteroids")
    #pygame.key.set_repeat(5)
 
    background_image = load_image('sprites/background-orig.png')
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()
    #myShip = ship.Ship('sprites/ship.png', 0.5, 10, True, 0, 0)
    myShip = SpriteSheet('sprites/ship.png', 0, 2, True, 0)
    explosion = SpriteSheet('sprites/bigexplosion.png', 1, 24, True, 1)
    debug = 0
    
    clock = pygame.time.Clock()
    screen.blit(background_image, (0, 0))
   
    while True:
        time = clock.tick(30)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)

        
            if eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_q:   
                    explosion = SpriteSheet('sprites/bigexplosion.png', 3
                    , 24, True, 1)
                if eventos.key == pygame.K_a:   
                    myShip.frame = 1
            if eventos.type == pygame.KEYUP:
                if eventos.key == pygame.K_a:     
                    myShip.frame = 0
        if keys[K_m]:
            myShip.angle -=4
        if keys[K_n]:
            myShip.angle +=4

    ##############################draw area#############################
        #draw background
        screen.blit(background_image, (0, 0))
        #scroll background
        screen.blit(scrolling_bg_image, back_rect) 
        screen.blit(scrolling_bg_image, back_rect.move(back_rect.width, 0)) 
        back_rect.move_ip(-1, 0)
        if back_rect.right == 0:
            back_rect.x = 0
        #draw ship
        ###myShip.render(screen)
        screen.blit(myShip.render(screen), (0,0)) 
        #explosion.render (screen)
        #draw fps text
        fps, fps_rect = texto (str(int(clock.get_fps())), 400,10, 14)
        screen.blit(fps, fps_rect)
        fps, fps_rect = texto (str(time), 500,10, 14)
        screen.blit(fps, fps_rect)
        fps, fps_rect = texto (str(debug), 700,10, 14)
        screen.blit(fps, fps_rect)

    ############################update area#############################
        myShip.update(time)
        explosion.update(time)
    #repaint
        pygame.display.flip()
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()