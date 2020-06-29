
# Módulos
import sys, pygame, os
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
    frames : list of number frames
    once: display anim once
    done: anim terminated
    '''
    def __init__(self, filename, speed, frames, once, frame, done = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(filename, True)
        self.rect = self.image.get_rect()      
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.frames = frames #number of frames
        self.once = once
        self.done = done
        self.frame = frame #current frame (zero-based)
        self.frameW = self.rect.width /frames
        self.frameH = self.rect.height
        self.surface = pygame.Surface

    def render(self, screen):
        rect_frame = (self.frame * self.frameW , 0, self.frameW, self.frameH)
        self.surface.blit(self.image, (0,0), (0,0,50,50) )
        return self.surface
    
    def update(self, dt):  
        if self.speed > 0:
            _frame = self.frame
            _frame = _frame  + (self.speed * dt)
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
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyAsteroids")
 
    background_image = load_image('sprites/background-orig.png')
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()
    #myShip = ship.Ship('sprites/ship.png', 0.5, 10, True, 0, 0)
    myShip = SpriteSheet('sprites/ship.png', 0, 2, True, True)
    
    clock = pygame.time.Clock()
    screen.blit(background_image, (0, 0))
   
    while True:
        time = clock.tick(30)
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        
        #draw background
        screen.blit(background_image, (0, 0))
        
        #scrolling background
        screen.blit(scrolling_bg_image, back_rect) 
        screen.blit(scrolling_bg_image, back_rect.move(back_rect.width, 0)) 
        back_rect.move_ip(-1, 0)
        if back_rect.right == 0:
            back_rect.x = 0

        
        #draw ship
        #screen.blit(myShip.render(), (0,0) )
        rectangle = (80,0,80,64)
        screen.blit(myShip.render(rectangle), (0,0) )

        #update screen
        pygame.display.flip()
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()