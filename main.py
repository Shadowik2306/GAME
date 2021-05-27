from sys_func import *
import pygame
import sqlite3
import random


pygame.init()
size = WIDTH, HEIGHT = 700, 700
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
final_score = 0


class Char:
    def __init__(self):
        self.percent = 50

    def change_per(self, n, k):
        self.percent += n
        try:
            self.image = pygame.transform.scale(load_image(f'char/{k}/{self.percent}%.png'),
                                                (75, 75))
            if self.percent == 100:
                raise Exception
            if self.percent == 0:
                raise Exception
        except Exception:
            print('Ты проиграл')
            print(f"Cчет: {final_score}", k)
            game_over(self.percent, k)

    def real_change(self):
        round = pygame.Surface((10, 10))
        pygame.draw.circle(round, (255, 255, 255), (5, 5), 5)
        screen.blit(round, (self.rect.x + 33, self.rect.y + 80))


class Church(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/church/{self.percent}%.png'),
                                            (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 330 - WIDTH // 10) * 0.5 - 20) * 1.3
        self.rect.y = int(HEIGHT * 0.02)


class Social(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/social/{self.percent}%.png'),
                                            (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 330 - WIDTH // 10) * 0.5 - 20) * 2
        self.rect.y = int(HEIGHT * 0.02)


class Army(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/army/{self.percent}%.png'),
                                            (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 330 - WIDTH // 10) * 0.5 - 20) * 2.9
        self.rect.y = int(HEIGHT * 0.02)


class Money(pygame.sprite.Sprite, Char):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image(f'char/money/{self.percent}%.png'),
                                            (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 330 - WIDTH // 10) * 0.5 - 20) * 3.6
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
        self.image = pygame.transform.scale(add_text(load_image(f'card/{self.choose[1]}.jpg', -1),
                                                     self.choose[0]), (250, 350))
        self.rect = self.image.get_rect()
        self.rect.x = 225
        self.rect.y = 200

    def update(self, *args, **kwargs):
        global LAST_POS, diff_with_card
        if LAST_POS:
            x = LAST_POS[0] - pygame.mouse.get_pos()[0]
            if pygame.mouse.get_pos()[0] not in range(int((WIDTH - 350 - WIDTH // 10) * 0.5),
                                                      int((WIDTH - 350 - WIDTH // 10) * 0.5
                                                          + 350 + WIDTH // 10) + 1):
                 x = 0
            self.rect.x -= x
            LAST_POS = (pygame.mouse.get_pos()[0], LAST_POS[1])
            if self.rect.x not in range(200, 350):
                font = pygame.font.SysFont(None, 25)
                if self.rect.x < 200:
                    text = self.choose[4].strip().capitalize()
                    lst = list(map(int, self.choose[2].split()))
                else:
                    text = self.choose[5].strip().capitalize()
                    lst = list(map(int, self.choose[3].split()))
                if lst[0]:
                    church.real_change()
                if lst[1]:
                    social.real_change()
                if lst[2]:
                    army.real_change()
                if lst[3]:
                    money.real_change()
                text = font.render(text, False, (0, 0, 0))
                screen.blit(text, (150, 550))
        else:
            self.rect.x = 225

    def check(self):
        global result, used, final_score
        if self.rect.x not in range(200, 350):
            if self.rect.x < 200:
                lst = list(map(int, self.choose[2].split()))
            else:
                lst = list(map(int, self.choose[3].split()))
            k = random.choice(range(len(result)))
            final_score += 1
            self.choose = result[k]
            used.append(result[k])
            del result[k]
            if not result:
                result = used.copy()
                used = []
            self.image = pygame.transform.scale(
                add_text(load_image(f'card/{self.choose[1]}.jpg', -1), self.choose[0]), (250, 350))
            self.rect = self.image.get_rect()
            self.rect.x = 225
            self.rect.y = 200
            church.change_per(lst[0], 'church')
            social.change_per(lst[1], 'social')
            army.change_per(lst[2], 'army')
            money.change_per(lst[3], 'money')



card = Card()


def set_background():
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    play_zone = pygame.Surface((350 + WIDTH // 10, HEIGHT))
    play_zone.fill((240, 214, 152))
    screen.blit(play_zone, ((WIDTH - 350 - WIDTH // 10) * 0.5, 0))
    upper = pygame.Surface((350 + WIDTH // 10, int(HEIGHT * 0.15)))
    upper.fill((122, 75, 56))
    screen.blit(upper, ((WIDTH - 350 - WIDTH // 10) * 0.5, 0))
    screen.blit(upper, ((WIDTH - 350 - WIDTH // 10) * 0.5, int(HEIGHT * 0.85)))


def game_over(n, k):
    global church, social, army, money, card, final_score, result, used
    fon = pygame.Surface((WIDTH, HEIGHT))
    fon.fill((0, 0, 0))
    screen.blit(fon, (0, 0))
    running = True
    font = pygame.font.SysFont(None, 40)
    if k == 'church':
        if n >= 100:
            text = [font.render('Вас распяли как святого', False, (255, 255, 255))]
        else:
            text = [font.render('Вас признали еретиком м сожгли', False, (255, 255, 255))]
    elif k == 'army':
        if n >= 100:
            text = [font.render('Армия захватила трон.', False,
                               (255, 255, 255))]
            text.append(font.render('Вы умерли в темнице от голода', False,
                               (255, 255, 255)))
        else:
            text = [font.render('Другая Страна захватила ваш трон.', False,
                               (255, 255, 255))]
            text.append(font.render('Вы теперь раб', False,
                               (255, 255, 255)))
    elif k == 'social':
        if n >= 100:
            text = [font.render('Вас задавила толпа фанатов и тиктокеров', False, (255, 255, 255))]
        else:
            text = [font.render('Вас отравили. Cмерть наступила через три дня', False,
                               (255, 255, 255))]
    elif k == 'money':
        if n >= 100:
            text = [font.render('Вы же знали, что гора золота не жидкость?', False, (255, 255, 255))]
        else:
            text = [font.render('Нужно больше золота!', False, (255, 255, 255))]
    y = 0
    for i in text:
        screen.blit(i, (0, y))
        y += 30

    text = font.render(f'Cчет: {final_score}', False, pygame.color.Color('white'))
    screen.blit(text, (0, y + 50))
    pygame.display.flip()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(church)
                    screen.fill((0, 0, 0))
                    set_background()
                    running = False
    all_sprites.empty()
    final_score = 0
    church = Church()
    social = Social()
    army = Army()
    money = Money()
    card = Card()
    result += used
    used = []


while True:
    set_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                diff_with_card = (card.rect.x - pygame.mouse.get_pos()[0]) * -1
                LAST_POS = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                LAST_POS = False
                card.check()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
