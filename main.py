
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

def writeText(screen, text, posX, posY,  size, center = True, color=(255, 255, 255), ):
    #font Press Start 2P Designed by CodeMan38 (Downloaded from googlefonts)
    fontfile = os.path.join (sys.path[0], 'fonts/font.ttf')
    font = pygame.font.Font(fontfile, size)
    renderedText = pygame.font.Font.render(font, text, 1, color)  
    renderedRect = renderedText.get_rect()
    if center:
        posX = posX - renderedRect.centerx
        posY = posY - renderedRect.centery
    screen.blit(renderedText, (posX, posY))

def angleToVector(ang):
    return [math.cos(ang * TO_RADIAN), math.sin(ang * TO_RADIAN)]

def offScreen (pos, width, height):
    if pos[0] + width < 0 or pos[0] > WIDTH or pos[1] > HEIGHT or pos[1]+ height < 0:
        return True
    return False

def collide(obj1, obj2):
    offset_x = int (obj2.pos[0] - obj1.pos[0])
    offset_y = int (obj2.pos[1] - obj1.pos[1])
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def randintS(limit): #randint from -limit to limit
    return randint(-limit, limit)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyAsteroids")
pygame.mixer.init()
background_image = load_image('sprites/background.png')

# ---------------------------------------------------------------------
def main():
    print (pygame.version.ver)
    #sounds
    bulletSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/missile.ogg"))
    explosionSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/explosion.ogg"))
    thrustSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/thrust.ogg"))
    alarmSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/alarm.ogg"))
    finalBoomSound = pygame.mixer.Sound(os.path.join (sys.path[0], "sounds/finalboom.ogg"))

    music = pygame.mixer.music.load(os.path.join (sys.path[0], "sounds/soundtrack.ogg"))
    
    #images
    bigAsteroidImg = load_image("sprites/asteroid.png", True)
    smallAsteroidImg =  load_image("sprites/smallasteroid.png", True) 
    shipImg =  load_image("sprites/fighter.png", True)
    tankImg =  load_image("sprites/shipcuadrado.png", True)
    bulletImg =  load_image("sprites/bullet.png", True)
    bigRedExplosionImg =  load_image("sprites/bigredexplosion.png", True)
    shieldImg = load_image("sprites/shield.png", True)
    redExplosionImg = load_image("sprites/redexplosion.png", True)
    finalExplosionImg = load_image("sprites/finalexplosion.png", True)
    scrolling_bg_image = load_image('sprites/scroll_bg.png')
    back_rect = scrolling_bg_image.get_rect()


    run = True
    countDownToGameOver = 120 #frames
    gameOverFlag = False
    score = 0
    fuel = 100
    deflector = 100
    tankEmpty = False
    tankOnGame = False
    explosions = []
    bullets = []
    bigAsteroids = []
    smallAsteroids = []
    ship = sh.SpriteSheet(shipImg, 0, 2, 1, True)
    ship.pos = [WIDTH//2 - ship.frameW//2, HEIGHT//2 - ship.frameH//2]
    tank = sh.SpriteSheet(tankImg, 0, 1, 1, True)
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
        
        #draw score
        writeText (screen, str(int(clock.get_fps())), 5,735, 14, False)
        writeText (screen, "Score: {}".format (score) , 20, 10, 24, False)

        #draw fuel
        writeText (screen, "Fuel" , 500, 20, 14)
        pygame.draw.rect(screen, (255,0,0), (450, 30 , 100, 10))
        pygame.draw.rect(screen, (0,255,0), (450, 30 , fuel, 10))

        #draw power Shield
        writeText (screen, "Deflector" , 900, 20, 14)
        pygame.draw.rect(screen, (255,0,0), (850, 30 , 100, 10))
        if deflector > 0:
            if deflector < 30: color = (255,165,0)
            else: color = (0,255,0)         
            pygame.draw.rect(screen, color, (850, 30 , deflector, 10))
        
        #repaint screen
        pygame.display.update()
    
    while run:
        time = clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        
        #randomly appearance of bigAsteroids
        #no more than 12 asteroids
        if len(bigAsteroids) < 4 + (score//500) and  not len(bigAsteroids) > 14 and not gameOverFlag:
            anAsteroid = sh.SpriteSheet(bigAsteroidImg, 0, 1, 1, True, randintS(MAX_ROT_ASTEROID))
            anAsteroid.pos = [randint(0,WIDTH), randint(0, HEIGHT)] 
            anAsteroid.vel = [randintS(MAX_VEL_ASTEROID), randintS(MAX_VEL_ASTEROID)]
            bigAsteroids.append (anAsteroid)

        #appearance of tank if running out of fuel and some random
        if  fuel < 40 and not tankOnGame and randint(0,100) < 10:
            tankOnGame = True
            tank.angle = randintS(70)
            tank.vel = angleToVector(tank.angle) * MAX_VEL_TANK

        #when not thrusting
        ship.setFrame(0)
        ship.vel[0] *= 0.95
        ship.vel[1] *= 0.95
        
        #Control keyboard
        if keys[K_q]: #debugging
            #global FPS
            #if FPS == 60: FPS = 5 
            #else: FPS = 60
            pass
        if keys[K_SPACE]: 
            if (pygame.time.get_ticks() - lastShot) > FPS * 4:
                acc = angleToVector(ship.angle)
                aBullet = sh.SpriteSheet(bulletImg, 0, 1, 1, True)
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
        if keys[K_s]: #right
            ship.angle -= SHIP_ROTATION_VEL
        if keys[K_a]: #left
            ship.angle += SHIP_ROTATION_VEL
        if keys[K_m]: #fire
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

        #resetting tank position and vel if tank goes offscreen
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
        deflector -= 0.01 * (score//1000) #deflector power decreases anyway with time and score
        for explosion in explosions[:]:
            explosion.update()
            if explosion.done:
                explosions.remove(explosion)
  
        if collide (ship, tank) and fuel < 100:
            fuel += 1
                 
        for bullet in bullets[:]:
            for bigAsteroid in bigAsteroids[:]:
                if collide (bullet, bigAsteroid):
                    explosionSound.play()
                    aExplosion = sh.SpriteSheet(bigRedExplosionImg, 1, 13, 1, True)
                    aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                    aExplosion.vel = [bigAsteroid.vel[0], bigAsteroid.vel[1]]
                    explosions.append (aExplosion)  
                    if deflector <100:
                        deflector+= 5                
                    #spawnLittleAsteroids
                    spawnlist = []
                    for i in range (3):
                        smallAsteroid = sh.SpriteSheet(smallAsteroidImg, 0, 1, 1, True, randintS(MAX_ROT_ASTEROID))
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
                        print ("error removing bullet with big asteroid")
                    score +=10

        for bullet in bullets[:]:
            for smallAsteroid in smallAsteroids[:]:
                if collide (bullet, smallAsteroid):
                    explosionSound.play()
                    aExplosion = sh.SpriteSheet(redExplosionImg, 1, 13, 1, True)
                    aExplosion.pos = [smallAsteroid.pos[0], smallAsteroid.pos[1]]
                    aExplosion.vel = [smallAsteroid.vel[0], smallAsteroid.vel[1]]
                    explosions.append (aExplosion)                  
                    smallAsteroids.remove(smallAsteroid)
                    if deflector <100:
                        deflector+= 10
                    try:
                        bullets.remove(bullet)
                    except:
                        print ("error removing bullet with small asteroid")
                    score +=50
        
        for bullet in bullets[:]:
            bullet.update()
            if offScreen(bullet.pos, bullet.frameW, bullet.frameH):
                bullets.remove(bullet)

        for bigAsteroid in bigAsteroids[:]:
            bigAsteroid.update()
            if collide(bigAsteroid, ship):
                #blowing up big asteroid 
                explosionSound.play()
                aExplosion = sh.SpriteSheet(bigRedExplosionImg, 1, 13, 1, True)
                aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                explosions.append (aExplosion)
                #shield explosion
                otherExplosion = sh.SpriteSheet(shieldImg, 0.5, 4, 4, True)                
                diffCenterX = otherExplosion.centerX-ship.centerX
                diffCenterY = otherExplosion.centerY-ship.centerY
                otherExplosion.pos = [ship.pos[0]-diffCenterX, ship.pos[1]-diffCenterX] 
                otherExplosion.vel = [ship.vel[0], ship.vel[1]]               
                explosions.append (otherExplosion)
                bigAsteroids.remove(bigAsteroid)
                deflector -=20
            if offScreen(bigAsteroid.pos, bigAsteroid.frameW, bigAsteroid.frameH):
                bigAsteroids.remove(bigAsteroid)

        for smallAsteroid in smallAsteroids[:]:
            smallAsteroid.update()
            if collide(smallAsteroid, ship):
                #blowing up small asteroid 
                explosionSound.play()
                aExplosion = sh.SpriteSheet(redExplosionImg, 1, 13, 1, True)
                aExplosion.pos = [bigAsteroid.pos[0], bigAsteroid.pos[1]]
                explosions.append (aExplosion)
                #ship shield explosion
                otherExplosion = sh.SpriteSheet(shieldImg, 0.5, 4, 4, True)
                diffCenterX = otherExplosion.centerX-ship.centerX
                diffCenterY = otherExplosion.centerY-ship.centerY
                otherExplosion.pos = [ship.pos[0]-diffCenterX, ship.pos[1]-diffCenterX] 
                otherExplosion.vel = [ship.vel[0], ship.vel[1]]
                explosions.append (otherExplosion)
                smallAsteroids.remove(smallAsteroid)
                deflector -= 10
            if offScreen(smallAsteroid.pos, smallAsteroid.frameW, smallAsteroid.frameH):
                smallAsteroids.remove(smallAsteroid)

        if deflector < 30 and deflector > 0:
            #SOUND ALARM
            alarmSound.play()

        if deflector < 0: 
            if not gameOverFlag:
                #stop all sounds
                alarmSound.stop()
                bulletSound.stop()
                explosionSound.stop()
                thrustSound.stop()
                #play finalSOUND
                finalBoomSound.play()
                bigFinalExplosion = sh.SpriteSheet(finalExplosionImg, 0.3 , 9, 9, True)
                bigFinalExplosion.pos = [ship.pos[0], ship.pos[1]]
                bigFinalExplosion.vel = [ship.vel[0], ship.vel[1]]
                explosions.append (bigFinalExplosion)
                bullets.clear()
                #explote remaining asteroids and tank (remaining items on screen)         
                allItems = (bigAsteroids + smallAsteroids)
                allItems.append(tank)
                for asteroid in allItems:
                    aExplosion = sh.SpriteSheet(bigRedExplosionImg, 0.5, 13, 1, True)
                    aExplosion.pos = [asteroid.pos[0], asteroid.pos[1]]
                    aExplosion.vel = [asteroid.vel[0], asteroid.vel[1]]
                    explosions.append (aExplosion)
                bigAsteroids.clear()
                smallAsteroids.clear()
                tank.done = True
                ship.done = True
                gameOverFlag = True
            #start countdown to gameover screen           
            countDownToGameOver -=0.5
            if countDownToGameOver < 0:
                gameOver()
     
    return 0

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        screen.blit(background_image, (0, 0))
        writeText (screen, "Insert Coin", WIDTH/2, 350, 30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

def gameOver():
    title_font = pygame.font.SysFont("comicsans", 70)
    coin_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        screen.blit(background_image, (0, 0))
        rectangle = pygame.Surface((WIDTH-300, HEIGHT-200)) 
        rectangle.set_alpha(50)            # alpha level
        rectangle.fill((255,0,0))           # this fills the entire surface
        screen.blit(rectangle, (150,100))    
        writeText (screen, "Game Over", WIDTH/2, 350, 60)
        writeText (screen, "Insert Coin", WIDTH/2, 550, 30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False           
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    return 0

 
if __name__ == '__main__':
    pygame.init()
    main_menu()