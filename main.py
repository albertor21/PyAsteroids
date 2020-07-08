
# Módulos
import sys, pygame, os
from random import randint
from pygame.locals import *
import spritesheet as sh
import math

# Constantes
FPS = 60
WIDTH = 1000
HEIGHT = 750
MAX_VEL_SHIP = 4 #ship's max velocity
MAX_VEL_TANK = 2
MAX_VEL_ASTEROID = 3
MAX_ROT_ASTEROID = 4
SHIP_ROTATION_VEL = 3
BULLET_SPEED = 30
TO_RADIAN = math.pi / 180



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

def randintS(limit): #randint from  -limit to limit
    return randint(-limit, limit)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyAsteroids")
pygame.mixer.init()
background_image = load_image('sprites/background.png')
background_image = load_image('sprites/background.png')

# ---------------------------------------------------------------------
def main():
    print (pygame.version.ver)
    
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()

    bulletSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/missile.ogg"))
    explosionSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/explosion.ogg"))
    thrustSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/thrust2.ogg"))
    music = pygame.mixer.music.load(os.path.join (sys.path[0], "sounds/soundtrack.ogg"))
    pygame.mixer.music.set_volume(0.3)

    run = True
    score = 0
    fuel = 100
    deflector = 10
    tankEmpty = False
    tankOnGame = False
    explosions = []
    bullets = []
    bigAsteroids = []
    smallAsteroids = []
    ship = sh.SpriteSheet('sprites/fighter.png', 0, 2, True)
    ship.pos = [WIDTH//2 - ship.frameW//2, HEIGHT//2 - ship.frameH//2]
    tank = sh.SpriteSheet('sprites/shipcuadrado.png', 0, 1, True)
    tank.pos = [-tank.frameW, randint(0, HEIGHT)] #Offscreen
    clock = pygame.time.Clock()
    lastShot = pygame.time.get_ticks()
    lastvelocity = [0,0]
    screen.blit(background_image, (0, 0))
    pygame.mixer.music.play(-1) # -1 will ensure the song keeps looping

    def redrawWindow(screen):
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
        #draw tank
        tank.render(screen)
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
        #livesTxt, livesTxtRect = texto ("Lives: {}".format (lives), WIDTH-100, 30, 32)
        #screen.blit(livesTxt, livesTxtRect)
        scoreTxt, scoreTxtRect = texto ("Score: {}".format (score) , 100, 30, 32)
        screen.blit(scoreTxt, scoreTxtRect)
        #draw fuel
        fuelTxt, fuelTxtRect = texto ("Fuel" , 505, 20, 22)
        screen.blit(fuelTxt, fuelTxtRect)
        pygame.draw.rect(screen, (255,0,0), (450, 30 , 100, 10))
        pygame.draw.rect(screen, (0,255,0), (450, 30 , fuel, 10))

        #draw power Shield
        deflectorTxt, deflectorTxtRect = texto ("Deflector" , 900, 20, 22)
        screen.blit(deflectorTxt, deflectorTxtRect)
        pygame.draw.polygon(screen, (255,0,0), ((850, 40) , (950,40), (950,30)))
        pygame.draw.polygon(screen, (0,255,0), ((850, 40) , (850 + deflector,40), (850 + deflector, 40 - deflector * 0.1)))
        
        #repaint screen
        pygame.display.update()
    
    while run:
        time = clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        
        #randomly appearance of bigAsteroids
        if len(bigAsteroids) < 4:
            anAsteroid = sh.SpriteSheet('sprites/asteroid.png', 0, 1, True, randintS(MAX_ROT_ASTEROID))
            anAsteroid.pos = [randint(0,WIDTH), randint(0, HEIGHT)] 
            anAsteroid.vel = [randintS(MAX_VEL_ASTEROID), randintS(MAX_VEL_ASTEROID)]
            bigAsteroids.append (anAsteroid)

        #appearance of tank if running out of fuel and chance
        if  fuel < 40 and not tankOnGame and randint(0,100) < 10:
            tankOnGame = True
            tank.angle = randintS(70)
            tank.vel = angleToVector(tank.angle) * MAX_VEL_TANK

        #when not thrusting
        ship.setFrame(0)
        ship.vel[0] *= 0.95
        ship.vel[1] *= 0.95
        
        #Control keyboard
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
                aBullet.vel = [BULLET_SPEED * acc[0], BULLET_SPEED * acc[1]]
                bullets.append (aBullet)
                lastShot = pygame.time.get_ticks()
                bulletSound.play()
        if keys[K_m]:
            ship.angle -= SHIP_ROTATION_VEL
        if keys[K_n]:
            ship.angle += SHIP_ROTATION_VEL
        if keys[K_a]: 
            ##Accelerate         
            if fuel > 0:
                acc = angleToVector(ship.angle)
                ship.vel[0] = ship.vel[0] + acc[0]
                if ship.vel[0] > MAX_VEL_SHIP: ship.vel[0] = MAX_VEL_SHIP
                if ship.vel[0] < -MAX_VEL_SHIP: ship.vel[0] = -MAX_VEL_SHIP
                ship.vel[1] = ship.vel[1] + acc[1] 
                if ship.vel[1] > MAX_VEL_SHIP: ship.vel[1] = MAX_VEL_SHIP
                if ship.vel[1] < -MAX_VEL_SHIP: ship.vel[1] = -MAX_VEL_SHIP
                ship.setFrame(1)
                thrustSound.play()
                lastvelocity[0] = ship.vel[0]
                lastvelocity[1] = ship.vel[1]
                fuel -= 0.15  
      
        #when decelerating
        if (abs(lastvelocity[0]) - abs(ship.vel[0])) > 1 or (abs(lastvelocity[1]) - abs(ship.vel[1])) > 1 :
            thrustSound.stop()
            
        #reappearing ship
        if (ship.pos[0] < 0):
            ship.pos[0] = WIDTH - ship.frameW
        ship.pos[0] = ship.pos[0] % WIDTH

        if (ship.pos[1] < 0):
            ship.pos[1] = HEIGHT - ship.frameH
        ship.pos[1] = ship.pos[1] % HEIGHT

        #resetting tank position and vel  if tank goes offscreen
        if (tank.pos[0] > WIDTH) or tank.pos[1] > HEIGHT:
            tank.pos = [-tank.frameW, randint(0, HEIGHT)] #Offscreen
            tank.vel = [0,0]
            tankOnGame = False
        

        if (ship.pos[1] < 0):
            ship.pos[1] = HEIGHT - ship.frameH
        ship.pos[1] = ship.pos[1] % HEIGHT


    ###########################draw area################################
        redrawWindow(screen)
    ############################update area#############################        
           
        tank.update()
        ship.update()
        for explosion in explosions[:]:
            explosion.update()
            if explosion.done:
                explosions.remove(explosion)
  
        if collide (ship, tank) and fuel < 100:
            fuel += 1

        if deflector < 0: 
            #run = False
            gameOver()

                    
        for bullet in bullets[:]:
            for bigAsteroid in bigAsteroids[:]:
                if collide (bullet, bigAsteroid):
                    explosionSound.play()
                    aExplosion = sh.SpriteSheet('sprites/bigredexplosion.png', 1, 13, True)
                    aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                    aExplosion.vel = [bigAsteroid.vel[0], bigAsteroid.vel[1]]
                    aExplosion.velRot = bigAsteroid.velRot
                    explosions.append (aExplosion)                  
                    #spawnLittleAsteroids
                    spawnlist = []
                    for i in range (3):
                        smallAsteroid = sh.SpriteSheet('sprites/smallasteroid.png', 0, 1, True, randintS(MAX_ROT_ASTEROID))
                        smallAsteroid.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                        spawnlist.append (smallAsteroid)
                    spawnlist[0].vel = [-randint(1,3), -randint(1,3)]
                    spawnlist[1].vel = [-randint(1,3), randint(1,3)]
                    spawnlist[2].vel = [randint(1,3), randint(1,3)]
                    for sa in spawnlist:
                        smallAsteroids.append (sa)
                    bigAsteroids.remove(bigAsteroid)
                    try:
                        bullets.remove(bullet)
                    except:
                        print ("error")
                    score +=10

        for bullet in bullets[:]:
            for smallAsteroid in smallAsteroids[:]:
                if collide (bullet, smallAsteroid):
                    explosionSound.play()
                    aExplosion = sh.SpriteSheet('sprites/redexplosion.png', 1, 13, True)
                    aExplosion.pos = [smallAsteroid.pos[0], smallAsteroid.pos[1]]
                    aExplosion.vel = [smallAsteroid.vel[0], smallAsteroid.vel[1]]
                    explosions.append (aExplosion)                  
                    smallAsteroids.remove(smallAsteroid)
                    if deflector <100:
                        deflector += 5
                    try:
                        bullets.remove(bullet)
                    except:
                        print ("error")
                    score +=50
        
        for bullet in bullets[:]:
            bullet.update()
            if offScreen(bullet.pos):
                bullets.remove(bullet)

        for bigAsteroid in bigAsteroids[:]:
            bigAsteroid.update()
            if collide(bigAsteroid, ship):
                #blowing up big asteroid 
                explosionSound.play()
                aExplosion = sh.SpriteSheet('sprites/bigredexplosion.png', 1, 13, True)
                aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                explosions.append (aExplosion)
                #blowing up ship 
                otherExplosion = sh.SpriteSheet('sprites/bigexplosion.png', 1, 24, True)
                otherExplosion.pos = [ship.pos[0], ship.pos[1]]
                explosions.append (otherExplosion)
                bigAsteroids.remove(bigAsteroid)
                deflector -=10
            if offScreen(bigAsteroid.pos):
                bigAsteroids.remove(bigAsteroid)

        for smallAsteroid in smallAsteroids[:]:
            smallAsteroid.update()
            if collide(smallAsteroid, ship):
                #blowing up small asteroid 
                explosionSound.play()
                aExplosion = sh.SpriteSheet('sprites/redexplosion.png', 1, 13, True)
                aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                explosions.append (aExplosion)
                #blowing up ship
                otherExplosion = sh.SpriteSheet('sprites/bigexplosion.png', 1, 24, True)
                otherExplosion.pos = [ship.pos[0], ship.pos[1]]
                explosions.append (otherExplosion)
                smallAsteroids.remove(smallAsteroid)
                deflector -= 5
                if deflector < 0: 
                    #run = False
                    gameOver()
            if offScreen(smallAsteroid.pos):
                smallAsteroids.remove(smallAsteroid)
     
    return 0

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        screen.blit(background_image, (0, 0))
        title_label = title_font.render("Insert Coin...", 1, (255,255,255))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

def gameOver():
    title_font = pygame.font.SysFont("comicsans", 70)
    coin = pygame.font.SysFont("comicsans", 40)
    #run = True
    #while run:
    screen.blit(background_image, (0, 0))
    pygame.draw.rect (screen, (125,125,125,100), (200,200, 600, 350))
    title_label = title_font.render("Game Over", 1, (255,0,0))
    screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
    coin_label = title_font.render("Insert Coin", 1, (255,255,255))
    screen.blit(coin_label, (WIDTH/2 - title_label.get_width()/2, 550))
    #pygame.display.update()
    #for event in pygame.event.get():
    #    if event.type == pygame.QUIT:
    #        run = False
    #    if event.type == pygame.MOUSEBUTTONDOWN:
    #        main()
    #pygame.quit()

 
if __name__ == '__main__':
    pygame.init()
    main_menu()