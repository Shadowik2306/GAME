import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def add_text(image, text):
    text = text.replace(',', '').strip().capitalize().split(' ')
    if len(text) > 3:
        change = len(text)
        i = 0
        for i in range(len(text) // 3):
            text[i] = ' '.join(text[i:i + 3])
            del text[i + 1]
            del text[i + 1]
        if change / 3 % 1 != 0:
            try:
                text[i + 1] = ' '.join(text[i + 1:])
                while True:
                    del text[i + 2]
            except Exception:
                pass
    else:
        text = [' '.join(text)]
    text_coord = 1000
    font = pygame.font.SysFont('Ariel', 65)
    for line in text:
        string_rendered = font.render(line, False, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 240
        text_coord += intro_rect.height
        image.blit(string_rendered, intro_rect)
    return image



def terminate():
    pygame.quit()
    sys.exit()