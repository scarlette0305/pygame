from pygame import *
from random import randint

#region creating variables
_WIDTH = 800
_HEIGHT = 640
window = display.set_mode((_WIDTH,_HEIGHT))
clock = time.Clock()
#endregion

#region creating classes
class GameSprite(sprite.Sprite):
    def __init__(self, filename, x,y, width, height,speed=0):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, (width,height))
        self.rect = Rect(x,y,width,height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        # move the player to the left or right
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        # control the player inside the window (not letting it goes out)
        if self.rect.x < 0 :
            self.rect.x = 0
        if self.rect.x > _WIDTH - self.rect.width:
            self.rect.x = _WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > _HEIGHT - self.rect.height:
            self.rect.y = _HEIGHT - self.rect.height

class Enemy(GameSprite):
    def update(self):
        global live
        # make the enemies move downwards
        self.rect.y += self.speed
        # if the enemies get out of the window, minus one point
        if self.rect.top > _HEIGHT:
            self.rect.x = randint(0, _WIDTH- self.rect.width)
            self.rect.y = 0
            live -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > _HEIGHT:
            self.rect.x = randint(0, _WIDTH- self.rect.width)
            self.rect.y = 0

#endregion
        
#region trivials      

live = 20
score = 0
# creating groups for each character
antas = sprite.Group()
fighter = sprite.Group() 
asteroids = sprite.Group()
# font and words
font.init()
f = font.SysFont(None, 70)
live_remain = f.render("Live remaining:" + str(live), True, (0,0,0))
score_having = f.render("Score: " + str(score), True, (0,255,255))
# applying the pictures into the window
game_over = GameSprite("lose_background.jpg",0,0,_WIDTH,_HEIGHT)
game_win = GameSprite('game_win.png',0,0,_WIDTH,_HEIGHT)
background = GameSprite("heaven.jpg", 0,0,_WIDTH, _HEIGHT)
prota = Player("evil.png", _WIDTH/2, _HEIGHT -95, 60,80, 10)    
# create the function for creating the enemies  
def create_anta():
    rand_speed = randint(1,3)
    anta = Enemy("angel.png", x=0, y=0, width=80,height=80,speed=rand_speed)
    anta.rect.x = randint(0, _WIDTH - anta.rect.width)
    anta.rect.bottom = 0
    antas.add(anta)
for i in range(8):
    create_anta()
# creating the function for creating the aliens
def create_asteroid():
    rand_speed = randint(1,2)
    asteroid = Asteroid("alien.png", x=0, y=0, width=80,height=80,speed=rand_speed)
    asteroid.rect.x = randint(0, _WIDTH - asteroid.rect.width)
    asteroid.rect.bottom = 0
    asteroids.add(asteroid)
for i in range(5):
    create_asteroid()
#endregion

live = 20
score = 0
death = False
game_is_running = True

#running the game
while game_is_running:
    if event.peek(QUIT):
        game_is_running = False
  
    
    background.draw(window)
    if not death:            
        prota.draw(window)
        prota.update()
        antas.draw(window)
        antas.update()            
        fighter.update()
        fighter.draw(window)
        live_remain = f.render("Live remaining:" + str(live), True, (0,0,0))
        score_having = f.render("Score: " + str(score), True, (0,255,255))
        window.blit(live_remain, (30,30))            
        window.blit(score_having,(30,80))
        asteroids.draw(window)
        asteroids.update()
        hits = sprite.groupcollide(fighter, antas, True,True)
        sprite.groupcollide(fighter, asteroids, True, False)
        for hit in hits:
            create_anta()
            score += 1
    if sprite.spritecollide(prota, asteroids, False):
        death = True
        live = 0
    if death:
        game_over.draw(window)
    
    if live <= 0:
        game_over.draw(window) 
        keys = key.get_pressed()  
        if keys[K_r]:
            death = False
            live = 20
            score = 0
            antas.empty()
            for i in range(6):
                create_anta()
            asteroids.empty()
            for i in range(5):
                create_asteroid()
    if score == 30:
        game_win.draw(window)
        keys = key.get_pressed()  
        if keys[K_r]:
            death = False
            live = 20
            score = 0
            antas.empty()
            for i in range(6):
                create_anta()
            asteroids.empty()
            for i in range(5):
                create_asteroid()
    for e in event.get():
        if e.type == KEYDOWN and e.key == K_SPACE:
            f1  = Bullet("broken heart.png", prota.rect.centerx , prota.rect.top, 40,35,speed=6)
            fighter.add(f1)            
    display.update()
    clock.tick(60)


