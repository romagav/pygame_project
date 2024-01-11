import pygame
from time import sleep
import sys
import os

pygame.init()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    img = pygame.image.load(fullname)
    if colorkey is not None:
        img = img.convert()
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey)
    else:
        img = img.convert_alpha()
    return img


def generate_level(level):
    number_of_enemy = 0
    number_of_bush = 0
    number_of_invis = 0
    win_tile, new_player, x, y, enemy, wall, invisible_tile = None, None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                number_of_bush -= 1
                wall = Tile('wall', x, y, number_of_bush)
            elif level[y][x] == '!':
                number_of_enemy += 1
                enemy = Enemy('enemy', x, y, number_of_enemy)
            elif level[y][x] == '*':
                win_tile = WinTile('win', x, y)
            elif level[y][x] == '%':
                number_of_invis += 1
                if number_of_invis <= number_of_enemy:
                    direction = number_of_invis + 1
                else:
                    direction = number_of_invis
                invisible_tile = InvisibleTile('invisible', x, y, direction)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return invisible_tile, win_tile, new_player, enemy, wall, x, y


fps = 60
clock = pygame.time.Clock()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
image = pygame.image.load('sand.png').convert_alpha()
image = pygame.transform.scale(image, (width, height))
screen.blit(image, (0, 0))
image_go = pygame.image.load('screen_gameover.png').convert_alpha()
image_go = pygame.transform.scale(image_go, (width, height))
image_nl = pygame.image.load('screen_nextlevel.png').convert_alpha()
image_nl = pygame.transform.scale(image_nl, (width, height))
image_end = pygame.image.load('screen_win.png').convert_alpha()
image_end = pygame.transform.scale(image_end, (width, height))
pygame.mixer.music.load('sizif.mp3')
pygame.mixer.music.play(-1)
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
win_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
invisible_group = pygame.sprite.Group()
enemys_group = pygame.sprite.Group()
cur_enemy = pygame.sprite.Group()
num_of_level = 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.png'), (800, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


tile_images = {
    'wall': load_image('bush.png'),
    'enemy': load_image('enemy.png'),
    'win': load_image('win_tile.png'),
    'invisible': load_image('invisible.png')
}
levels_names = {
    1: 'first_level.txt',
    2: 'second_level.txt',
}
player_image = load_image('ball.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, n):
        super().__init__(tiles_group, all_sprites)
        self.type = n
        image_1 = tile_images[tile_type]
        self.image = pygame.transform.scale(image_1, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, n):
        super().__init__(enemys_group, all_sprites)
        self.type = n
        image_1 = tile_images[tile_type]
        self.image = pygame.transform.scale(image_1, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class WinTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(win_group, all_sprites)
        image_1 = tile_images[tile_type]
        self.image = pygame.transform.scale(image_1, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class InvisibleTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, direction):
        super().__init__(invisible_group, all_sprites)
        image_1 = tile_images[tile_type]
        self.image = pygame.transform.scale(image_1, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.direction = direction


invisible_tile, win_tile, player, enemy, wall, level_x, level_y = generate_level(load_level('first_level.txt'))
up, down, right, left = False, False, False, False
running = True
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906:
                up = True
            if event.key == 1073741905:
                down = True
            if event.key == 1073741903:
                right = True
            if event.key == 1073741904:
                left = True

        if event.type == pygame.KEYUP:
            if event.key == 1073741906:
                up = False
            if event.key == 1073741905:
                down = False
            if event.key == 1073741903:
                right = False
            if event.key == 1073741904:
                left = False
    if up:
        player.rect.top -= 1
    if down:
        player.rect.top += 1
    if right:
        player.rect.left += 1
    if left:
        player.rect.left -= 1
    screen.blit(image, (0, 0))

    if pygame.sprite.spritecollideany(player, invisible_group):
        for i in invisible_group:
            if pygame.sprite.collide_rect(player, i):
                n = i.direction
        for spr in enemys_group:
            if spr.type == n:
                spr.add(cur_enemy)
        player_group.draw(screen)
        win_group.draw(screen)
        tiles_group.draw(screen)
        cur_enemy.draw(screen)
        pygame.display.flip()
        cur_enemy.empty()
    if pygame.sprite.spritecollideany(player, tiles_group) or pygame.sprite.spritecollideany(player, enemys_group):
        if pygame.sprite.spritecollideany(player, tiles_group):
            for spr in tiles_group:
                if pygame.sprite.collide_mask(player, spr):
                    screen.blit(image_go, (0, 0))
                    pygame.display.flip()
                    sleep(2)
                    player.kill()
                    invisible_tile, win_tile, player, enemy, wall, level_x, level_y = generate_level(
                        load_level(levels_names[num_of_level]))
                    break
        else:
            if pygame.sprite.spritecollideany(player, enemys_group):
                screen.blit(image_go, (0, 0))
                pygame.display.flip()
                sleep(2)
                player.kill()
                invisible_tile, win_tile, player, enemy, wall, level_x, level_y = generate_level(
                    load_level(levels_names[num_of_level]))
    if pygame.sprite.spritecollideany(player, win_group):
        player.kill()
        for spr in all_sprites:
            spr.kill()
        num_of_level += 1
        if num_of_level == 3:
            screen.blit(image_end, (0, 0))
            pygame.display.flip()
            sleep(5)
            running = False
        else:
            screen.blit(image_nl, (0, 0))
            pygame.display.flip()
            sleep(4)
            invisible_tile, win_tile, player, enemy, wall, level_x, level_y = generate_level(
                load_level(levels_names[num_of_level]))
    clock.tick(fps)
    player_group.draw(screen)
    win_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
pygame.quit()
