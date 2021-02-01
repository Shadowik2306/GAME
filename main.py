from sys_func import *
import pygame


pygame.init()
size = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

LAST_POS = False
CENTER = (WIDTH // 2, HEIGHT // 2)


class Church(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image('char/church/0%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 1.2
        self.rect.y = int(HEIGHT * 0.02)


class Social(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image('char/social/0%.png'), (125, 110))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 1.95
        self.rect.y = int(HEIGHT * 0.02) - 5


class Army(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image('char/army/0%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 2.7
        self.rect.y = int(HEIGHT * 0.02) - 5


"""class Money(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.percent = 50
        self.image = pygame.transform.scale(load_image('char/army/0%.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = ((WIDTH - 500 - WIDTH // 10) * 0.5 - 20) * 2.7
        self.rect.y = int(HEIGHT * 0.02) - 5"""


class Card(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((300, 400))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 325

    def update(self, *args, **kwargs):
        global LAST_POS, diff_with_center
        if LAST_POS:
            print(diff_with_center)
            if LAST_POS[0] - pygame.mouse.get_pos()[0] != 0:
                x = LAST_POS[0] - (LAST_POS[0] - pygame.mouse.get_pos()[0])
                self.rect.x = x + diff_with_center
                LAST_POS = (self.rect.x, LAST_POS[1])





church = Church()
social = Social()
army = Army()
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
            diff_with_center = (CENTER[0] - pygame.mouse.get_pos()[0]) * -1
            LAST_POS = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            LAST_POS = False
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()