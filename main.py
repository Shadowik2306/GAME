from sys_func import *
import pygame
import sqlite3
import random


pygame.init()
size = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

LAST_POS = False
CENTER = (WIDTH // 2, HEIGHT // 2)

con = sqlite3.connect('data/card/Cards.db')
cur = con.cursor()
result = list((cur.execute("""SELECT * FROM cards""").fetchall()))
used = []


class Char:
    def __init__(self):
        self.percent = 50

    def change_per(self, n, k):
        self.percent += n
        try:
            self.image = pygame.transform.scale(load_image(f'char/{k}/{self.percent}%.png'), (100, 100))
        except Exception:
            print('Ты проиграл')
            sys.exit(-1)


class Church(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/church/{self.percent}%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 1.3
        self.rect.y = int(HEIGHT * 0.02)


class Social(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/social/{self.percent}%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 2
        self.rect.y = int(HEIGHT * 0.02)


class Army(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/army/{self.percent}%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 2.9
        self.rect.y = int(HEIGHT * 0.02)


class Money(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/money/{self.percent}%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 3.6
        self.rect.y = int(HEIGHT * 0.02)


church = Church()
social = Social()
army = Army()
money = Money()


class Card(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        k = random.choice(range(len(result)))
        self.choose = result[k]
        used.append(result[k])
        del result[k]
        self.image = pygame.transform.scale(add_text(load_image(f'card/{self.choose[1]}.jpg', -1), self.choose[0]), (300, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 325

    def update(self, *args, **kwargs):
        global LAST_POS, diff_with_card
        if LAST_POS:
            x = LAST_POS[0] - pygame.mouse.get_pos()[0]
            if pygame.mouse.get_pos()[0] not in range(int((WIDTH - 500 - WIDTH // 10) * 0.5),
                                                      int((WIDTH - 500 - WIDTH // 10) * 0.5
                                                          + 500 + WIDTH // 10) + 1):
                return
            self.rect.x -= x
            LAST_POS = (pygame.mouse.get_pos()[0], LAST_POS[1])
        else:
            self.rect.x = 350

    def check(self):
        global result, used
        if self.rect.x not in range(300, 450):
            if self.rect.x < 300:
                lst = list(map(int, self.choose[2].split()))
            else:
                lst = list(map(int, self.choose[3].split()))
            k = random.choice(range(len(result)))
            self.choose = result[k]
            used.append(result[k])
            del result[k]
            if not result:
                result = used.copy()
                used = []
            self.image = pygame.transform.scale(
                add_text(load_image(f'card/{self.choose[1]}.jpg', -1), self.choose[0]), (300, 400))
            self.rect = self.image.get_rect()
            self.rect.x = 350
            self.rect.y = 325
            church.change_per(lst[0], 'church')
            social.change_per(lst[1], 'social')
            army.change_per(lst[2], 'army')
            money.change_per(lst[3], 'money')


card = Card()


def set_background():
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    play_zone = pygame.Surface((500 + WIDTH // 10, HEIGHT))
    play_zone.fill((240, 214, 152))
    screen.blit(play_zone, ((WIDTH - 500 - WIDTH // 10) * 0.5, 0))
    upper = pygame.Surface((500 + WIDTH // 10, int(HEIGHT * 0.15)))
    upper.fill((122, 75, 56))
    screen.blit(upper, ((WIDTH - 500 - WIDTH // 10) * 0.5, 0))
    screen.blit(upper, ((WIDTH - 500 - WIDTH // 10) * 0.5, int(HEIGHT * 0.85)))


while True:
    set_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            diff_with_card = (card.rect.x - pygame.mouse.get_pos()[0]) * -1
            LAST_POS = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            LAST_POS = False
            card.check()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()