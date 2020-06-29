 
# Módulos
import sys, pygame, os
from pygame.locals import *
 
# Constantes
WIDTH = 800
HEIGHT = 600
 
# Clases
# ---------------------------------------------------------------------
class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, filename, speed, frames, once, index, frame, done = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(filename, True)
        self.rect = self.image.get_rect()      
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.frames = frames #number of frames
        self.once = once
        self.done = done
        self.frame = frame #current frame
        self.frameW = self.rect.width /frames
        self.frameH = self.rect.height
        
    def render(self, screen):
    
    #var frame;
    #    if (this.speed > 0) {
    #      var max = this.frames.length;
    #      var idx = Math.floor(this._index);
    #      frame = this.frames[idx % max];
    #      if (this.once && idx >= max) {
    #        this.done = true;
    #        return;
    #      }
    #    } else {
    #      frame = this._frame;
    #    }

    #    var x = this.pos[0];
    #    var y = this.pos[1];
    #    var w = this.size[0];
    #    var h = this.size[1];
        rect_frame = x,self.frame *,self.frameW, self.frameH
        screen.blit(self.image, (0,0), rect_frame )
    
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
    pygame.display.set_caption("Pruebas PyAsteroids")
 
    background_image = load_image('sprites/background.png')
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()
    ship = Ship('sprites/ship.png', 0.5, 10, True, 0, 0)
    
 
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
        #screen.blit(ship.render(), (0,0) )
        ship.render(screen)
        #screen.blit(ship.image, (0,0) )

        #update screen
        pygame.display.flip()
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()