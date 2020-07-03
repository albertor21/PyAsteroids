
# Módulos
import sys, pygame, os

from pygame.locals import *
import spritesheet as sh
import math


# Constantes
WIDTH = 800
HEIGHT = 600
TO_RADIAN = math.pi / 180;

 
# Clases
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
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


def texto(texto, posx, posy,  size, color=(255, 255, 255)):
    fontfile = os.path.join (sys.path[0], 'fonts/ledger-Regular.ttf')
    fuente = pygame.font.Font(fontfile, size)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def angleToVector(ang):
    return [math.cos(ang * TO_RADIAN), math.sin(ang * TO_RADIAN)]

 
# ---------------------------------------------------------------------

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyAsteroids")
    #pygame.key.set_repeat(5)
 
    background_image = load_image('sprites/background-orig.png')
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()
    explosionList= []
    ship = sh.SpriteSheet('sprites/ship.png', 0, 2, True, 0)
    explosion = sh.SpriteSheet('sprites/bigexplosion.png', 3, 24, True, 1)
    
    
    clock = pygame.time.Clock()
    screen.blit(background_image, (0, 0))
   
    while True:
        time = clock.tick(30)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)

        
           #if eventos.type == pygame.KEYDOWN:
           #    if eventos.key == pygame.K_q:   
           #        explosion = SpriteSheet('sprites/bigexplosion.png', 3, 24, True, 1)

           #if eventos.type == pygame.KEYUP:
                pass

        ship.setFrame(0)
        ship.vel[0] *= 0.99
        ship.vel[1] *= 0.99
        
        if keys[K_q]:
            explosion = sh.SpriteSheet('sprites/bigexplosion.png', 3, 24, True, 1)
        if keys[K_m]:
            ship.angle -=4
        if keys[K_n]:
            ship.angle +=4
        if keys[K_a]:           
            acc = angleToVector(ship.angle);
            ship.vel[0] += (acc[0]) #% maxVel;
            ship.vel[1] -= (acc[1]) #% maxVel;
            ship.setFrame(1)

        if (ship.pos[0] < 0):
            ship.pos[0] = WIDTH - ship.frameW

        ship.pos[0] = ship.pos[0] % WIDTH

        if (ship.pos[1] < 0):
            ship.pos[1] = HEIGHT - ship.frameH

        ship.pos[1] = ship.pos[1] % HEIGHT;

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
        ship.render(screen)
        #screen.blit(myShip.render(), (400, 300)) 
        explosion.render (screen)
        #screen.blit(explosion.render(), (200, 300)) 
        #draw fps text
        fps, fps_rect = texto (str(int(clock.get_fps())), 400,10, 14)
        screen.blit(fps, fps_rect)
        fps, fps_rect = texto (str(time), 500,10, 14)
        screen.blit(fps, fps_rect)
        fps, fps_rect = texto (str(ship.angle), 700,10, 14)
        screen.blit(fps, fps_rect)

    ############################update area#############################
        ship.update()
        explosion.update()
    #repaint
        pygame.display.flip()
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()