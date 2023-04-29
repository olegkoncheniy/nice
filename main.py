from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
background = transform.scale(image.load('back.jpg'), (700, 500))

schet = 0
lose = 0
win = 0
no = 0
yes = 0


class Game_comunism(sprite.Sprite):
    def __init__(self, picture, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.height = height
        self.width = width

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


lost = 0


class Game_nacist_enemy(Game_comunism):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.width - 5)
            lost += 1


class Player(Game_comunism):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - self.width - 5:
            self.rect.x += self.speed
        if keys[K_LSHIFT]:
            self.speed = 20
        if not keys[K_LSHIFT]:
            self.speed = 10

    def fire(self):
        bulled = Bullet('pngegg.png', self.rect.centerx, self.rect.top, -10, 15, 20)
        bulets.add(bulled)


class Bullet(Game_comunism):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


bulets = sprite.Group()

enemys = sprite.Group()
enemy1 = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 1, 65, 65)
enemy2 = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 4, 65, 65)
enemy3 = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 5, 65, 65)
enemy4 = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 3, 65, 65)
enemy5 = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 7, 65, 65)

asteroids = sprite.Group()
astareoid1 = Game_nacist_enemy("pngegg (1).png", randint(0, 700 - 65 - 5), 0, 1, 65, 65)
astareoid2 = Game_nacist_enemy("pngegg (1).png", randint(0, 700 - 65 - 5), 0, 1, 65, 65)
astareoid3 = Game_nacist_enemy("pngegg (1).png", randint(0, 700 - 65 - 5), 0, 1, 65, 65)

asteroids.add(astareoid1)
asteroids.add(astareoid2)
asteroids.add(astareoid3)

enemys.add(enemy1)
enemys.add(enemy2)
enemys.add(enemy3)
enemys.add(enemy4)
enemys.add(enemy5)

avtomat = Player('avtomat.png', 350, 400, 10, 100, 80)

font.init()
font1 = font.Font(None, 30)

mixer.init()
mixer.music.load('fon.ogg')
mixer.music.play()
kick = mixer.Sound('krik.ogg')
clock = time.Clock()

win_t = font1.render("ты уничтожил всех гитлеров", True, (0, 0, 0))
lose_t = font1.render("гилеры захватили вселенную", True, (0, 0, 0))

num_fire = 0
rel_time = False

game_negr = True
finish = False
while game_negr:
    if finish != True:

        window.blit(background, (0, 0))

        avtomat.reset()
        avtomat.update()

        enemys.draw(window)
        enemys.update()

        asteroids.draw(window)
        asteroids.update()

        bulets.draw(window)
        bulets.update()

        if rel_time == True:
            nom_time = timer()


            if nom_time - last_time < 3:
                reload = font1.render('Мне надо перезаррядится', 1, (150, 0, 0))
                window.blit(reload,(260, 460))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(avtomat, enemys, False):
            finish = True
            window.blit(lose_t, (800, 400))

        sprite_list = sprite.groupcollide(enemys, bulets, True, True)
        for i in sprite_list:
            schet += 1
            enemy = Game_nacist_enemy("pngwing.com (2).png", randint(0, 700 - 65 - 5), 0, 1, 65, 65)
            enemys.add(enemy)
            #kick.play()

        text_lose = font1.render("-" + str(lost) + " рублей с твоего баланса", True, (0, 0, 0))
        window.blit(text_lose, (20, 20))

        negr_die = font1.render("-" + str(schet) + " убито негров:", True, (0, 0, 0))
        window.blit(negr_die, (20, 40))

        if lost >= 20000:
            finish = True
            window.blit(lose_t, (800, 400))

        if schet >= 10:
            finish = True
            window.blit(win_t, (800, 400))

    for e in event.get():
        if e.type == QUIT:
            game_negr = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    avtomat.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    display.update()
    clock.tick(60)
