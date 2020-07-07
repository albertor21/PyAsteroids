
# Módulos
import sys, pygame, os
import random
from pygame.locals import *
import spritesheet as sh
import math


# Constantes
WIDTH = 1000
HEIGHT = 750
MAXVELSHIP = 15 #ship's max velocity
MAXVELASTEROID = 3# 15 #ship's max velocity
BULLETSPEED = 50
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

def offScreen (pos):
    if pos[0] < 0 or pos[0] > WIDTH or pos[1] > HEIGHT or pos[1] < 0:
        return True
    return False

def distance (pos1, pos2):
    return (Math.sqrt(Math.pow(pos2[0] - pos1[0], 2) + Math.pow(pos2[1] - pos1[1], 2)))

def collide(obj1, obj2):
    offset_x = int (obj2.pos[0] - obj1.pos[0])
    offset_y = int (obj2.pos[1] - obj1.pos[1])
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def gameOver(screen):
    pygame.draw.rect (screen, (125,125,125,100), (200,200, 600, 350))
 
# ---------------------------------------------------------------------

def main():
    print (pygame.version.ver)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyAsteroids")
    pygame.mixer.init()
    background_image = load_image('sprites/backgroundB.png')
    scrolling_bg_image = load_image('sprites/scroll_bgB.png')
    back_rect = scrolling_bg_image.get_rect()

    bulletSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/missile.ogg"))
    explosionSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/explosion.ogg"))
    thrustSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/thrust2.ogg"))
    music = pygame.mixer.music.load(os.path.join (sys.path[0], "sounds/soundtrack.ogg"))
    pygame.mixer.music.set_volume(0.3)

    run = True
    lives = 3
    score = 0
    fuel = 100
    explosions = []
    bullets = []
    bigAsteroids = []
    smallAsteroids = []
    ship = sh.SpriteSheet('sprites/fighter.png', 0, 2, True)
    clock = pygame.time.Clock()
    lastShot = pygame.time.get_ticks()
    lastvelocity = [0,0]
    screen.blit(background_image, (0, 0))
    pygame.mixer.music.play(-1) # -1 will ensure the song keeps looping
    while run:
        time = clock.tick(30)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        
        #randomly appearance of bigAsteroids
        if random.randint(0,1) < 1- math.pow (0.993, pygame.time.get_ticks()) and len(bigAsteroids) < 5:
            anAsteroid = sh.SpriteSheet('sprites/asteroid.png', 0, 1, True, random.randint(-4, 4))
            anAsteroid.pos = [random.randint(0,WIDTH), random.randint(0, HEIGHT)]
            anAsteroid.vel = [random.randint(-1,1), random.randint(-1,1)]
            bigAsteroids.append (anAsteroid)

        #when not thrusting
        ship.setFrame(0)
        ship.vel[0] *= 0.95
        ship.vel[1] *= 0.95
        
        #Control keyboard
        if keys[K_q]:
            explosionSound.play()
            aExplosion = sh.SpriteSheet('sprites/redexplosion.png', 1, 13, True, 1)
            aExplosion.pos = [random.randint(0,WIDTH), random.randint (0, HEIGHT)]
            explosions.append (aExplosion)
        if keys[K_SPACE]: 
            if (pygame.time.get_ticks() - lastShot) > 150:
                acc = angleToVector(ship.angle)
                aBullet = sh.SpriteSheet('sprites/bullet.png', 0, 1, True)
                halfFrameWS = ship.frameW // 2 + 1
                halfFrameHS = ship.frameH // 2 + 1
                halfFrameWB = aBullet.frameW // 2 + 1
                halfFrameHB = aBullet.frameH // 2 + 1
                centerX = ship.pos[0] + halfFrameWS
                centerY = ship.pos[1] + halfFrameHS
                #la punta del cañon
                pointX = centerX + halfFrameWS * acc[0]
                pointY = centerY - halfFrameHS * acc[1]               
                aBullet.pos = [pointX - halfFrameWB, pointY -halfFrameHB]
                aBullet.angle = ship.angle
                aBullet.vel = [BULLETSPEED * acc[0], BULLETSPEED * acc[1]]
                bullets.append (aBullet)
                lastShot = pygame.time.get_ticks()
                bulletSound.play()
        if keys[K_s]:
            ship.angle -= 6
        if keys[K_a]:
            ship.angle += 6
        if keys[K_m]: 
            ##Accelerate         
            if fuel > 0:
                acc = angleToVector(ship.angle)
                ship.vel[0] = ship.vel[0] + acc[0]
                if ship.vel[0] > MAXVELSHIP: ship.vel[0] = MAXVELSHIP
                if ship.vel[0] < -MAXVELSHIP: ship.vel[0] = -MAXVELSHIP
                ship.vel[1] = ship.vel[1] + acc[1] 
                if ship.vel[1] > MAXVELSHIP: ship.vel[1] = MAXVELSHIP
                if ship.vel[1] < -MAXVELSHIP: ship.vel[1] = -MAXVELSHIP
                ship.setFrame(1)
                thrustSound.play()
                lastvelocity[0] = ship.vel[0]
                lastvelocity[1] = ship.vel[1]
                fuel -= 0.15  
      
        #when decelerating
        if (abs(lastvelocity[0]) - abs(ship.vel[0])) > 1 or (abs(lastvelocity[1]) - abs(ship.vel[1])) > 1 :
            thrustSound.stop()
            
        #reappearing 
        if (ship.pos[0] < 0):
            ship.pos[0] = WIDTH - ship.frameW
        ship.pos[0] = ship.pos[0] % WIDTH

        if (ship.pos[1] < 0):
            ship.pos[1] = HEIGHT - ship.frameH
        ship.pos[1] = ship.pos[1] % HEIGHT


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
        #draw bullets
        for bullet in bullets:
            bullet.render(screen)
        #draw explosions
        for explosion in explosions:
            explosion.render(screen)

        #draw asteroids
        for bigAsteroid in bigAsteroids:
            bigAsteroid.render(screen)

        for smallAsteroid in smallAsteroids:
            smallAsteroid.render(screen)
        
        #draw fps text
        fps, fps_rect = texto (str(int(clock.get_fps())), 30,700, 14)
        screen.blit(fps, fps_rect)
        #fps, fps_rect = texto (str(len(bullets)), 500,10, 14)
        #screen.blit(fps, fps_rect)
        livesTxt, livesTxtRect = texto ("Lives: {}".format (lives), WIDTH-100, 30, 32)
        screen.blit(livesTxt, livesTxtRect)
        scoreTxt, scoreTxtRect = texto ("Score: {}".format (score) , 100, 30, 32)
        screen.blit(scoreTxt, scoreTxtRect)
        fuelTxt, fuelTxtRect = texto ("Fuel" , 505, 20, 22)
        screen.blit(fuelTxt, fuelTxtRect)
        #draw Fuel
        pygame.draw.rect(screen, (255,0,0), (450, 30 , 100, 10))
        pygame.draw.rect(screen, (0,255,0), (450, 30 , fuel, 10))

    ############################update area#############################        
        ship.update()
        for explosion in explosions[:]:
            explosion.update()
            if explosion.done:
                explosions.remove(explosion)

        for bullet in bullets[:]:
            for bigAsteroid in bigAsteroids[:]:
                if collide (bullet, bigAsteroid):
                    explosionSound.play()
                    aExplosion = sh.SpriteSheet('sprites/bigredexplosion.png', 1, 13, True)
                    aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                    aExplosion.vel = [bigAsteroid.vel[0], bigAsteroid.vel[1]]
                    aExplosion.velRot = bigAsteroid.velRot
                    explosions.append (aExplosion)
                    bigAsteroids.remove(bigAsteroid)
                    try:
                        bullets.remove(bullet)
                    except:
                        print ("error")
                    score +=10
        
        for bullet in bullets[:]:
            bullet.update()
            if offScreen(bullet.pos):
                bullets.remove(bullet)
               
        for smallAsteroid in smallAsteroids[:]:
            smallAsteroid.update()
            if offScreen(smallAsteroid.pos):
                smallAsteroid.remove(smallAsteroid)

        for bigAsteroid in bigAsteroids[:]:
            bigAsteroid.update()
            if collide(bigAsteroid, ship):
                explosionSound.play()
                aExplosion = sh.SpriteSheet('sprites/bigredexplosion.png', 1, 13, True)
                aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                explosions.append (aExplosion)
                otherExplosion = sh.SpriteSheet('sprites/redexplosion.png', 1, 13, True)
                otherExplosion.pos = [ship.pos[0], ship.pos[1]]
                explosions.append (otherExplosion)
                bigAsteroids.remove(bigAsteroid)
                lives -=1
                if lives == 0: 
                    #run = False
                    gameOver(screen)
            if offScreen(bigAsteroid.pos):
                bigAsteroids.remove(bigAsteroid)

    #repaint screen
        pygame.display.update()
        
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()