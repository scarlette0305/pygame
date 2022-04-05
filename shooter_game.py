from pygame import *
from random import randint

#region variables
_WIDTH = 800
_HEIGHT = 640
live = 20
score = 0
window = display.set_mode((_WIDTH,_HEIGHT))
clock = time.Clock()
#endregion


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
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
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
        self.rect.y += self.speed
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
        
#region trivials      

live = 20
score = 0
font.init()
f = font.SysFont(None, 70)
live_remain = f.render("Live remaining:" + str(live), True, (0,0,0))
score_having = f.render("Score: " + str(score), True, (0,255,255))
introductory_sentence = f.render("You are evils and you're taking over the heaven", True, (255,255,255))
introductory_sentence2 = f.render("Press the space bar to shoot the angels", True, (255,255,255))
introductory_sentence0 = f.render("Press 'ENTER' to start playing", True, (255,255,255))
antas = sprite.Group()
fighter = sprite.Group() 
asteroids = sprite.Group()
introduction = GameSprite("welcome.png",0,0,_WIDTH,_HEIGHT)   
game_over = GameSprite("lose_background.jpg",0,0,_WIDTH,_HEIGHT)
game_win = GameSprite('game_win.png',0,0,_WIDTH,_HEIGHT)
background = GameSprite("heaven.jpg", 0,0,_WIDTH, _HEIGHT)
prota = Player("evil.png", _WIDTH/2, _HEIGHT -95, 60,80, 10)      
def create_anta():
    rand_speed = randint(1,3)
    anta = Enemy("angel.png", x=0, y=0, width=80,height=80,speed=rand_speed)
    anta.rect.x = randint(0, _WIDTH - anta.rect.width)
    anta.rect.bottom = 0
    antas.add(anta)
def create_asteroid():
    asteroid = Asteroid("alien.png", x=0, y=0, width=80,height=80,speed=1)
    asteroid.rect.x = randint(0, _WIDTH - asteroid.rect.width)
    asteroid.rect.bottom = 0
    asteroids.add(asteroid)
for i in range(8):
    create_anta()
for i in range(5):
    create_asteroid()
#endregion

live = 20
score = 0
death = False
game_is_running = True

while game_is_running:
    
    for e in event.get():
        if e.type == QUIT:
            game_is_running = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            f1  = Bullet("broken heart.png", prota.rect.centerx , prota.rect.top, 40,35,speed=6)
            fighter.add(f1)
    
    #introduction.draw(window)
    #introductory_sentence = f.render("You are evils and you're taking over the heaven", True, (255,255,255))
    #introductory_sentence2 = f.render("Press the space bar to shoot the angels", True, (255,255,255))
    #introductory_sentence3 = f.render("Press 'ENTER' to start playing", True, (255,255,255))
    #window.blit(introductory_sentence, (100,100))
    #window.blit(introductory_sentence2, (150,150))
    #window.blit(introductory_sentence3, (200,200))
    #keys = key.get_pressed()
    #if keys[K_e]:
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
        window.blit(score_having,(30,60))
        asteroids.draw(window)
        asteroids.update()
        hits = sprite.groupcollide(fighter, antas, True,True)
        sprite.groupcollide(fighter, asteroids, True, False)
    if sprite.spritecollide(prota, asteroids, False):
        game_over.draw(window)
    if death:
        game_over.draw(window)
    for hit in hits:
        create_anta()
        score += 1
    if live <= 0:
        game_over.draw(window) 
        keys = key.get_pressed()  
        if keys[K_r]:
            death = False
            antas.empty()
            for i in range(6):
                create_anta()
    if score == 20:
        game_win.draw(window)
        keys = key.get_pressed()  
        if keys[K_d]:
            death = False
            antas.empty()
            for i in range(6):
                create_anta()
                
    display.update()
    clock.tick(60)


