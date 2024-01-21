import pygame
import random as ran
import sqlite3
import time
pygame.init()

# upload music and sounds
pygame.mixer.music.load('sounds/tanchiki_fon_music.mp3')
pygame.mixer.music.set_volume(0.1)
sound_shoot = pygame.mixer.Sound('sounds/tanchiki_vistrel.wav')
sound_shoot.set_volume(0.5)
sound_uncht_tanka = pygame.mixer.Sound('sounds/tanchili_vzriv_tanka.wav')
sound_uncht_tanka.set_volume(0.6)
sound_hit_on_tank = pygame.mixer.Sound('sounds/tanchiki_hit_on_tank.wav')
sound_hit_on_tank.set_volume(0.2)
sound_medkit = pygame.mixer.Sound('sounds/tanchiki_medkit.wav')
sound_medkit.set_volume(0.5)
sound_boost = pygame.mixer.Sound('sounds/tanchiki_boost.wav')
sound_boost.set_volume(0.15)

# connect db
conn = sqlite3.connect('tanchiki_database.sql')
cur = conn.cursor()

W = 600
H = 600
FPS = 30
clock_ = pygame.time.Clock()
pygame.display.set_caption('TANCHIKI')
scr = pygame.display.set_mode((W, H))

# upload images
pygame.display.set_icon(pygame.image.load('images/tanchiki/icon_tanchiki.ico'))
bg = pygame.image.load('images/tanchiki/bg_tanki.png').convert()
bg_pause = pygame.image.load('images/tanchiki/bg_pause_game_tanki.png').convert()
boost_img = pygame.image.load('images/tanchiki/boost.png').convert_alpha()
boost_img_or = pygame.image.load('images/tanchiki/boost_or.png').convert_alpha()
medkit_img_or = pygame.image.load('images/tanchiki/medkit_or.png').convert_alpha()
bullet_img = pygame.image.load('images/tanchiki/bullet_tank.png').convert_alpha()
effects_img = [pygame.image.load('images/tanchiki/effect_shield.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_slow.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_teleport.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_speed.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_-1hp.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_+1att.png').convert_alpha()
               ]
main_disp_img = pygame.image.load('images/tanchiki/main_disp.png').convert_alpha()
medkit_img = pygame.image.load('images/tanchiki/medkit.png').convert_alpha()
nastr_spravka_bg_img = pygame.image.load('images/tanchiki/nastroiki_spravka.png').convert_alpha()
spravka_img = pygame.image.load('images/tanchiki/spravka.png').convert_alpha()
tank_img, tank1_img = pygame.image.load('images/tanchiki/tank.png').convert_alpha(), \
    pygame.image.load('images/tanchiki/tank1.png').convert_alpha()
tank_razr_img, tank1_razr_img = pygame.image.load('images/tanchiki/tank1_razr.png').convert_alpha(),\
    pygame.image.load('images/tanchiki/tank2_razr.png').convert_alpha()
wall_img = pygame.image.load('images/tanchiki/wall_tank.png').convert_alpha()
zvuk_on_img, zvuk_off_img = pygame.image.load('images/tanchiki/zvuk_tanchiki_on.png').convert_alpha(),\
    pygame.image.load('images/tanchiki/zvuk_tanchiki_off.png').convert_alpha()
tank1_hp = pygame.image.load('images/tanchiki/tank1_hp.png').convert_alpha()
tank2_hp = pygame.image.load('images/tanchiki/tank2_hp.png').convert_alpha()

# upload fonts
font_schet = pygame.font.Font('Fonts/Intro.ttf', 15)
font_st_disp = pygame.font.Font('Fonts/PsychicForce2012Monospaced.ttf', 40)
font_sprav_main_nastr = pygame.font.Font('Fonts/PsychicForce2012Monospaced.ttf', 120)


class Boosts(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_an = boost_img
        self.image = boost_img_or
        self.frame = 0
        self.rect = self.image.get_rect()
        self.killed = False
        self.rect.x, self.rect.y = ran.randint(0, 9) * 60, ran.randint(1, 9) * 60
        while pygame.sprite.spritecollide(self, walls, False) or pygame.sprite.spritecollide(self, tanks, False):
            self.rect.x, self.rect.y = ran.randint(0, 9) * 60, ran.randint(1, 9) * 60

    def update(self):
        global Sopric_boost, Sopric_tank
        hits_boost = pygame.sprite.spritecollide(self, tanks, False)
        if hits_boost:
            sound_boost.play()
            Sopric_boost = True
            Sopric_tank = hits_boost[0]
            self.dokill()

    def draw(self):
        if not self.killed:
            self.frame = (self.frame + 0.3) % 7
            scr.blit(boost_img, (self.rect.x, self.rect.y), (30 * int(self.frame), 0, 30, 30))

    def dokill(self):
        self.killed = True
        self.kill()


class Medkit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_an = medkit_img
        self.image = medkit_img_or
        self.rect = self.image.get_rect()
        self.killed = False
        self.frame = 0
        self.rect.x, self.rect.y = ran.randint(0, 9) * 60 + 5, ran.randint(1, 9) * 60 + 5
        while pygame.sprite.spritecollide(self, walls, False) or pygame.sprite.spritecollide(self, tanks, False) or\
                pygame.sprite.spritecollide(self, boosts, False):
            self.rect.x, self.rect.y = ran.randint(0, 9) * 60 + 5, ran.randint(1, 9) * 60 + 5

    def update(self):
        hits_medkit = pygame.sprite.spritecollide(self, tanks, False)
        if hits_medkit and hits_medkit[0].hp != 5:
            sound_medkit.play()
            if hits_medkit[0].hp < 4:
                hits_medkit[0].hp += 2
            else:
                hits_medkit[0].hp = 5
            self.dokill()

    def draw(self):
        if not self.killed:
            self.frame = (self.frame + 0.05) % 2
            scr.blit(medkit_img, (self.rect.x, self.rect.y), (20 * int(self.frame), 0, 20, 20))

    def dokill(self):
        self.killed = True
        self.kill()


class Tank1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank_img
        self.image_orig = self.image
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.image_dead = tank1_razr_img
        self.rect = self.image.get_rect()
        self.rect.x = 9 * 60 + 30
        self.rect.y = ran.randint(1, 9) * 60
        self.speed = 2
        self.pos = 1
        self.hp = 5
        self.shield = 0
        self.attack = 1

    def update(self):
        old_x, old_y = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left < 0:
                self.rect.left = 0
            self.rect.x -= self.speed
            self.image = self.image_left
            self.pos = 2
        elif keys[pygame.K_RIGHT]:
            if self.rect.right > 600:
                self.rect.right = 600
            self.rect.x += self.speed
            self.image = self.image_right
            self.pos = 4
        elif keys[pygame.K_UP]:
            if self.rect.top < 32:
                self.rect.top = 32
            self.rect.y -= self.speed
            self.image = self.image_orig
            self.pos = 1
        elif keys[pygame.K_DOWN]:
            if self.rect.bottom > 600:
                self.rect.bottom = 600
            self.rect.y += self.speed
            self.image = self.image_down
            self.pos = 3
        stolk_walls = pygame.sprite.spritecollide(tank_2, walls, False)
        stolk_tanks = pygame.sprite.collide_rect(tank_1, tank_2) if tank_1 in tanks else None
        if stolk_walls or stolk_tanks:
            self.rect.x, self.rect.y = old_x, old_y

    def shoot(self):
        bull = Bullet2(self.rect.centerx, self.rect.centery, self.pos)
        all_sprites.add(bull)
        bullets.add(bull)
        bullets_t_2.add(bull)

    def is_live(self):
        if self.hp <= 0:
            self.dokill()
        scr.blit(pygame.transform.rotate(self.image_dead, (self.pos - 1) * 90), (self.rect.x, self.rect.y))

    def dokill(self):
        tanks.remove(tank_2)
        all_sprites.remove(tank_2)
        self.kill()


class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank1_img
        self.image_orig = self.image
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.image_dead = tank_razr_img
        self.rect = self.image.get_rect()
        self.rect.x = 0 * 60
        self.rect.y = ran.randint(1, 9) * 60
        self.speed = 2
        self.pos = 1
        self.hp = 5
        self.shield = 0
        self.attack = 1

    def update(self):
        old_x, old_y = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.rect.left < 0:
                self.rect.left = 0
            self.rect.x -= self.speed
            self.image = self.image_left
            self.pos = 2
        elif keys[pygame.K_d]:
            if self.rect.right > 600:
                self.rect.right = 600
            self.rect.x += self.speed
            self.image = self.image_right
            self.pos = 4
        elif keys[pygame.K_w]:
            if self.rect.top < 32:
                self.rect.top = 32
            self.rect.y -= self.speed
            self.image = self.image_orig
            self.pos = 1
        elif keys[pygame.K_s]:
            if self.rect.bottom > 600:
                self.rect.bottom = 600
            self.rect.y += self.speed
            self.image = self.image_down
            self.pos = 3
        stolk_walls = pygame.sprite.spritecollide(tank_1, walls, False)
        stolk_tanks = pygame.sprite.collide_rect(tank_1, tank_2) if tank_2 in tanks else None
        if stolk_walls or stolk_tanks:
            self.rect.x, self.rect.y = old_x, old_y

    def shoot(self):
        bull = Bullet1(self.rect.centerx, self.rect.centery, self.pos)
        all_sprites.add(bull)
        bullets.add(bull)
        bullets_t_1.add(bull)

    def is_live(self):
        if self.hp <= 0:
            self.dokill()
        scr.blit(pygame.transform.rotate(self.image_dead, (self.pos - 1) * 90), (self.rect.x, self.rect.y))

    def dokill(self):
        tanks.remove(tank_1)
        all_sprites.remove(tank_1)
        self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, x_block, y_block):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_block, y_block
        self.hp = 1

    def update(self):
        if self.hp < 1:
            self.dokill()

    def dokill(self):
        x_t, y_t = self.rect.x // 30, self.rect.y // 30
        pole_of_blocks[x_t][y_t] = ''
        self.kill()


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x_bull, y_bull, pos_bull):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image_orig = self.image
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.pos = pos_bull
        self.speed = 10
        if pos_bull == 1:
            self.rect.bottom = y_bull
            self.rect.centerx = x_bull
        elif pos_bull == 2:
            self.rect.top = y_bull - 3
            self.rect.centerx = x_bull
            self.image = self.image_left
        elif pos_bull == 3:
            self.rect.top = y_bull
            self.rect.centerx = x_bull
            self.image = self.image_down
        elif pos_bull == 4:
            self.rect.bottom = y_bull + 3
            self.rect.centerx = x_bull
            self.image = self.image_right

    def update(self):
        if self.pos == 1:
            self.rect.y -= self.speed
            if self.rect.y < 32:
                self.kill()
        elif self.pos == 2:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.kill()
        elif self.pos == 3:
            self.rect.y += self.speed
            if self.rect.y > 600:
                self.kill()
        elif self.pos == 4:
            self.rect.x += self.speed
            if self.rect.x > 600:
                self.kill()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x_bull, y_bull, pos_bull):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image_orig = self.image
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.pos = pos_bull
        self.speed = 10
        if pos_bull == 1:
            self.rect.bottom = y_bull
            self.rect.centerx = x_bull
        elif pos_bull == 2:
            self.rect.top = y_bull - 3
            self.rect.centerx = x_bull
            self.image = self.image_left
        elif pos_bull == 3:
            self.rect.top = y_bull
            self.rect.centerx = x_bull
            self.image = self.image_down
        elif pos_bull == 4:
            self.rect.bottom = y_bull + 3
            self.rect.centerx = x_bull
            self.image = self.image_right

    def update(self):
        if self.pos == 1:
            self.rect.y -= self.speed
            if self.rect.y < 32:
                self.kill()
        elif self.pos == 2:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.kill()
        elif self.pos == 3:
            self.rect.y += self.speed
            if self.rect.y > 600:
                self.kill()
        elif self.pos == 4:
            self.rect.x += self.speed
            if self.rect.x > 600:
                self.kill()


class StartDisplay:
    def __init__(self):
        self.option_menu = []
        self.callbacks = []
        self.tek_index = 0

    def append_option(self, option, callback):
        self.option_menu.append(font_st_disp.render(option, True, (0, 0, 0)))
        self.callbacks.append(callback)

    def switch(self, direct):
        self.tek_index = max(0, min(self.tek_index + direct, len(self.option_menu) - 1))

    def select(self):
        self.callbacks[self.tek_index]()

    def drawi(self, x_dr, y_dr, option_y_padding):
        for i_dr, option in enumerate(self.option_menu):
            option_rect = option.get_rect()
            option_rect.topleft = (x_dr, y_dr + i_dr * option_y_padding)
            if i_dr == self.tek_index:
                pygame.draw.rect(scr, (255, 255, 255), option_rect)
            scr.blit(option, option_rect)


class Settings:
    def __init__(self):
        self.option_menu = []
        self.callbacks = []
        self.rezhimi = []
        self.tek_index = 0

    def append_option(self, option, callback):
        self.option_menu.append(font_st_disp.render(option, True, (0, 0, 0)))
        self.callbacks.append(callback)
        self.rezhimi.append(True)

    def switch(self, direct):
        self.tek_index = max(0, min(self.tek_index + direct, len(self.option_menu) - 1))

    def select(self):
        self.rezhimi[self.tek_index] = not self.rezhimi[self.tek_index]
        game_pause_cls.rezhimi[0] = self.rezhimi[0]
        self.callbacks[self.tek_index]()

    def drawi(self, x_dr, y_dr, option_y_padding):
        for i_dr, option in enumerate(self.option_menu):
            option_rect = option.get_rect()
            option_rect.topleft = (x_dr, y_dr + i_dr * option_y_padding)
            if i_dr == self.tek_index:
                pygame.draw.rect(scr, (255, 255, 255), option_rect)
            scr.blit(option, option_rect)
            if self.rezhimi[i_dr]:
                scr.blit(zvuk_on_img, (540, 300 + i_dr * option_y_padding))
            else:
                scr.blit(zvuk_off_img, (540, 300 + i_dr * option_y_padding))


class GamePause:
    def __init__(self):
        self.option_menu_txt = []
        self.option_menu = []
        self.callbacks = []
        self.rezhimi = []
        self.tek_index = 0

    def append_option(self, option, callback, nastr=False):
        self.option_menu_txt.append(option)
        self.option_menu.append(font_st_disp.render(option, True, (0, 0, 0)))
        self.callbacks.append(callback)
        if nastr:
            self.rezhimi.append(settings.rezhimi[0])

    def switch(self, direct):
        self.tek_index = max(0, min(self.tek_index + direct, len(self.option_menu) - 1))

    def select(self):
        if self.option_menu_txt[self.tek_index] == 'звук':
            self.rezhimi[0] = not settings.rezhimi[0]
            settings.rezhimi[0] = not settings.rezhimi[0]
        self.callbacks[self.tek_index]()

    def drawi(self, x_dr, y_dr, option_y_padding):
        for i_dr, option in enumerate(self.option_menu):
            option_rect = option.get_rect()
            option_rect.topleft = (x_dr, y_dr + i_dr * option_y_padding)
            if i_dr == self.tek_index:
                pygame.draw.rect(scr, (255, 255, 255), option_rect)
            scr.blit(option, option_rect)
            if self.option_menu_txt[i_dr] == 'звук':
                if self.rezhimi[0]:
                    scr.blit(zvuk_on_img, (540, 300 + i_dr * option_y_padding))
                else:
                    scr.blit(zvuk_off_img, (540, 300 + i_dr * option_y_padding))


def switch_volume():
    if settings.rezhimi[0]:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.unpause()
        sound_shoot.set_volume(0.5)
        sound_uncht_tanka.set_volume(0.6)
        sound_boost.set_volume(0.15)
        sound_hit_on_tank.set_volume(0.2)
        sound_medkit.set_volume(0.5)
    else:
        pygame.mixer.music.pause()
        sound_shoot.set_volume(0)
        sound_uncht_tanka.set_volume(0)
        sound_boost.set_volume(0)
        sound_hit_on_tank.set_volume(0)
        sound_medkit.set_volume(0)


def start_game():
    global perezapusk
    perezapusk = True
    switch_volume()


# def start_online_game():
#     global f_online_game
#     f_online_game = True


def switch_game_pause():
    global game_pause, game_pause_f, start_time_boost, current_time_boost, start_time_shoot_tank1, \
        start_time_shoot_tank2
    game_pause, game_pause_f = False, False
    start_time_boost = time.time() - current_time_boost
    start_time_shoot_tank1 = time.time() - current_time_tank1
    start_time_shoot_tank2 = time.time() - current_time_tank2


def main_menu():
    global perezapusk, game_f, game_pause_f
    game_pause_cls.tek_index = 0
    perezapusk, game_f, game_pause_f = False, False, False


def quit_game():
    global st_ekran
    st_ekran = False
    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 1))
    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 2))
    conn.commit()
    cur.close()
    conn.close()


def spravka():
    global f_spravka
    f_spravka = True


def nastroiki():
    global f_nastroiki
    f_nastroiki = True


menu = StartDisplay()
st_ekran = True
f_online_game = False
perezapusk = False
f_spravka = False
f_nastroiki = False
obsh_vol = True
cur.execute('SELECT * FROM tanks')
schet = cur.fetchall()
menu.append_option('НАЧАТЬ ИГРУ', lambda: start_game())
# menu.append_option('Сетевая игра (бета)', lambda: start_online_game())
menu.append_option('справка', lambda: spravka())
menu.append_option('настройки', lambda: nastroiki())
menu.append_option('ВЫЙТИ ИЗ ИГРЫ', lambda: quit_game())
settings = Settings()
settings.append_option('ЗВУК', lambda: switch_volume())
game_pause_cls = GamePause()
game_pause_cls.append_option('продолжить', lambda: switch_game_pause())
game_pause_cls.append_option('звук', lambda: switch_volume(), True)
game_pause_cls.append_option('выйти в меню', lambda: main_menu())
while st_ekran:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 1))
            cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 2))
            conn.commit()
            cur.close()
            conn.close()
            st_ekran = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if f_nastroiki:
                    settings.switch(-1)
                else:
                    menu.switch(-1)
            if event.key == pygame.K_DOWN:
                if f_nastroiki:
                    settings.switch(1)
                else:
                    menu.switch(1)
            if event.key == pygame.K_SPACE:
                if f_nastroiki:
                    settings.select()
                else:
                    menu.select()
            if event.key == pygame.K_ESCAPE:
                f_spravka = False
                f_nastroiki = False
    if f_spravka:
        scr.blit(nastr_spravka_bg_img, (0, 0))
        scr.blit(spravka_img, (0, 0))
        txt_sprv = font_st_disp.render('справка', True, (14, 103, 24))
        scr.blit(txt_sprv, (W // 2 - txt_sprv.get_width() // 2, 0))
    elif f_nastroiki:
        scr.blit(main_disp_img, (0, 0))
        txt_settings = font_sprav_main_nastr.render('Settings', True, (255, 255, 255))
        scr.blit(txt_settings, (W // 2 - txt_settings.get_width() // 2, 0))
        settings.drawi(335, 300, 50)
    else:
        scr.blit(main_disp_img, (0, 0))
        menu.drawi(335, 300, 50)
        txt_name = font_sprav_main_nastr.render('TANCHIKI', True, (255, 255, 255))
        scr.blit(txt_name, (W // 2 - txt_name.get_width() // 2, 0))
    if not perezapusk:
        sound_shoot.set_volume(0)
        sound_uncht_tanka.set_volume(0)
        sound_boost.set_volume(0)
        sound_hit_on_tank.set_volume(0)
        sound_medkit.set_volume(0)
        pygame.mixer.music.stop()
    pygame.display.update()
    while perezapusk:
        pole_of_blocks = [['' for i in range(20)] for _ in range(20)]
        all_sprites = pygame.sprite.Group()
        tanks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullets_t_1 = pygame.sprite.Group()
        bullets_t_2 = pygame.sprite.Group()
        walls = pygame.sprite.Group()
        boosts = pygame.sprite.Group()
        medkits = pygame.sprite.Group()
        tank_1 = Tank()
        tank_2 = Tank1()
        all_sprites.add(tank_1)
        all_sprites.add(tank_2)
        tanks.add(tank_1)
        tanks.add(tank_2)
        start_time_shoot_tank1 = time.time()
        start_time_shoot_tank2 = time.time()
        start_time_mk = time.time()
        for i in range(100):
            x, y = ran.randint(0, 19) * 30, ran.randint(1, 19) * 30
            while (x == tank_1.rect.x and y == tank_1.rect.y) or (x == tank_2.rect.x and y == tank_2.rect.y):
                x, y = ran.randint(0, 19) * 30, ran.randint(1, 19) * 30
            wall = Block(x, y)
            pole_of_blocks[x // 30][y // 30] = wall
            all_sprites.add(wall)
            walls.add(wall)
        boost = Boosts()
        boosts.add(boost)

        game_f = True
        boost_f = True
        can_shoot_tank2 = False
        can_shoot_tank1 = False
        start_time_boost = 0
        rand_baff = 0
        f_medkit = False
        Sopric_boost = False
        Eff_boost = False
        live_is = True
        game_pause = False
        Sopric_tank = Tank()
        current_time_tank1 = 1
        current_time_tank2 = 1
        current_time_mk = 10
        current_time_boost = 0
        shetchik_mk = 0

        while game_f:
            if can_shoot_tank2:
                current_time_tank2 = int(time.time() - start_time_shoot_tank2)
            if can_shoot_tank1:
                current_time_tank1 = int(time.time() - start_time_shoot_tank1)
            if f_medkit:
                current_time_mk = int(time.time() - start_time_mk)
            if Sopric_boost:
                Eff_boost = True
                sp_baffs = [4]
                rand_baff = ran.choice(sp_baffs)
                start_time_boost = time.time()
                if rand_baff == 1:
                    Sopric_tank.shield = 1
                elif rand_baff == 2:
                    Sopric_tank.speed = 1
                elif rand_baff == 3:
                    Sopric_tank.rect.topleft = ran.randint(0, 9) * 60, ran.randint(1, 9) * 60
                    while pygame.sprite.groupcollide(tanks, walls, False, False) or \
                            pygame.sprite.collide_rect(tank_2, tank_1):
                        Sopric_tank.rect.topleft = ran.randint(0, 9) * 60, ran.randint(1, 9) * 60
                elif rand_baff == 4:
                    Sopric_tank.rect.topleft = boost.rect.topleft
                    Sopric_tank.speed = 5
                elif rand_baff == 5:
                    Sopric_tank.hp -= 1
                elif rand_baff == 6:
                    Sopric_tank.attack = 2
                Sopric_boost = False
            if len(medkits) < 3:
                if current_time_mk == 10 and shetchik_mk < 5:
                    shetchik_mk += 1
                    medkit = Medkit()
                    medkits.add(medkit)
                    start_time_mk = time.time()
                    current_time_mk = 0
                f_medkit = True
            if len(medkits) >= 3:
                current_time_mk = 0
                start_time_mk = time.time()
                f_medkit = False
            if current_time_tank1 == 1:
                can_shoot_tank1 = False
                current_time_tank1 = 1
            if current_time_tank2 == 1:
                can_shoot_tank2 = False
                current_time_tank2 = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 1))
                    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 2))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st_ekran = False
                    perezapusk = False
                    game_f = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and tank_1 in tanks:
                        if current_time_tank1 == 1:
                            start_time_shoot_tank1 = time.time()
                            can_shoot_tank1 = True
                            tank_1.shoot()
                            sound_shoot.play()
                    if event.key == pygame.K_l and tank_2 in tanks:
                        if current_time_tank2 == 1:
                            start_time_shoot_tank2 = time.time()
                            can_shoot_tank2 = True
                            tank_2.shoot()
                            sound_shoot.play()
                    if event.key == pygame.K_ESCAPE:
                        game_pause = True
            if game_pause:
                game_pause_f = 1
                scr.blit(bg_pause, (0, 0))
                while game_pause_f:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 1))
                            cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (0, 2))
                            conn.commit()
                            cur.close()
                            conn.close()
                            st_ekran = False
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                game_pause_cls.switch(-1)
                            if event.key == pygame.K_DOWN:
                                game_pause_cls.switch(1)
                            if event.key == pygame.K_SPACE:
                                game_pause_cls.select()
                            if event.key == pygame.K_ESCAPE:
                                game_pause_f = 0
                                game_pause = False
                                start_time_boost = time.time() - current_time_boost
                        scr.blit(main_disp_img, (0, 0))
                        txt_su = font_sprav_main_nastr.render('Pause', True, (255, 255, 255))
                        scr.blit(txt_su, (W // 2 - txt_su.get_width() // 2, 0))
                        game_pause_cls.drawi(335, 300, 50)
                        pygame.display.update()

            all_sprites.update()
            boosts.update()
            medkits.update()
            scr.blit(bg, (0, 0))

            if Eff_boost:
                if not game_pause:
                    current_time_boost = int(time.time() - start_time_boost)
                if current_time_boost < 20:
                    if Sopric_tank == tank_2:
                        scr.blit(effects_img[rand_baff - 1], (600 - (30 * (tank_2.hp + 1)) + 2, 2))
                    elif Sopric_tank == tank_1:
                        scr.blit(effects_img[rand_baff - 1], (abs(30 * tank_1.hp) + 2, 2))
                else:
                    g = tank_img if Sopric_tank == tank_2 else tank1_img
                    Sopric_tank.image_orig = g
                    Sopric_tank.image_left = pygame.transform.rotate(g, 90)
                    Sopric_tank.image_right = pygame.transform.rotate(g, -90)
                    Sopric_tank.image_down = pygame.transform.rotate(g, 180)
                    Sopric_tank.speed = 2
                    Sopric_tank.attack = 1
                    Eff_boost = False
            if len(tanks) == 1:
                cur.execute('SELECT * FROM tanks')
                schet = cur.fetchall()
                if tank_1 in tanks:
                    value = int(schet[0][1]) + 1
                    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (value, 1))
                    conn.commit()
                elif tank_2 in tanks:
                    value = int(schet[1][1]) + 1
                    cur.execute(f'UPDATE tanks SET value = ? WHERE id_tank = ?', (value, 2))
                    conn.commit()
                cur.execute('SELECT * FROM tanks')
                schet = cur.fetchall()
                time.sleep(1.5)
                break
            if len(tanks) == 0:
                time.sleep(1.5)
                break
            if pygame.sprite.groupcollide(walls, bullets, False, False):
                for i in pygame.sprite.groupcollide(walls, bullets, False, True):
                    i.hp -= 1
            if pygame.sprite.spritecollide(tank_1, bullets_t_2, True):
                if tank_1.shield > 0:
                    tank_1.shield = -1
                else:
                    tank_1.hp -= tank_2.attack
                sound_hit_on_tank.play()
            if pygame.sprite.spritecollide(tank_2, bullets_t_1, True):
                if tank_2.shield > 0:
                    tank_2.shield = -1
                else:
                    tank_2.hp -= tank_1.attack
                sound_hit_on_tank.play()
            if live_is:
                if tank_1.hp <= 0:
                    tank_1.is_live()
                    sound_uncht_tanka.play()
                elif tank_2.hp <= 0:
                    tank_2.is_live()
                    sound_uncht_tanka.play()

            # drawing all
            all_sprites.draw(scr)
            if not Eff_boost:
                boost.draw()
            for i in medkits:
                i.draw()

            txt_surf = font_schet.render(str(f'Синий {schet[0][1]} : {schet[1][1]} Красный'), True, 'White')
            scr.blit(txt_surf, (W // 2 - txt_surf.get_width() // 2, 5))
            scr.blit(tank1_hp, (0, 0), (abs(30 * (tank_1.hp - 5)), 0, 150, 30))
            scr.blit(tank2_hp, (W - 150, 0), ((30 * (tank_2.hp - 5)), 0, 150, 30))

            pygame.display.update()
            clock_.tick(FPS)