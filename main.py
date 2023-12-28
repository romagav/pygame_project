import pygame
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
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                Tile('enemy', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


size = width, height = 800, 400
screen = pygame.display.set_mode(size)
image = pygame.image.load('sand.png').convert_alpha()
screen.blit(image, (0, 0))
pygame.mixer.music.load('sizif.mp3')
pygame.mixer.music.play()
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('bush.png'),
    'enemy': load_image('enemy.png')
}
player_image = load_image('ball.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player, level_x, level_y = generate_level(load_level('first_level.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == 1073741906:
                player.rect.top -= 10
            if event.key == 1073741905:
                player.rect.top += 10
            if event.key == 1073741903:
                player.rect.left += 10
            if event.key == 1073741904:
                player.rect.left -= 10
        screen.blit(image, (0, 0))
        pygame.display.flip()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
