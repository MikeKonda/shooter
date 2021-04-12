#Создай собственный Шутер!
from random import randint
from pygame import *
font.init()
font2 = font.SysFont('Arial', 36)
mixer.init()
#mixer.music.load('space.ogg')
fire_s = mixer.Sound('fire.ogg')
#mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def Fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(10, 690)
            missed += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
ship =  Player('rocket.png', win_width//2, win_height-100, 80, 100, 5)
ufos = sprite.Group()
for e in range(1,6):
    ufo = Enemy("ufo.png", randint(10, 690), 0, 80, 50, randint(1, 2))
    ufos.add(ufo)
bullets = sprite.Group()


score = 0
missed = 0

win = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE!', True, (250, 0, 0))

game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get(): 
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.Fire()
                fire_s.play()
    if finish != True:
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy("ufo.png", randint(10, 690), 0, 80, 50, randint(1, 2))
            ufos.add(ufo)
        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text2 = font2.render('Пропущенно: ' + str(missed), 1, (255, 255, 255))
        window.blit(background, (0, 0))
        window.blit(text, (10,10))
        window.blit(text2, (10,35))
        ship.update()
        ship.reset()
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
    if sprite.spritecollide(ship, ufos, False) or missed >= 3:
        finish = True
        window.blit(lose, (10,65))
    if score >= 10:
        finish = True
        window.blit(win, (10,65))
    display.update()
    clock.tick(FPS)