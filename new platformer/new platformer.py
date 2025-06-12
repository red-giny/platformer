import pygame
from pygame.locals import *

pygame.init()

font = pygame.font.SysFont('Lobster', 70)
font_score = pygame.font.SysFont('Lobster', 30)

tile_size = 50
game_over = 0
menu = True
shop_screen = False
next_level = False
coins = 50
level_index = 0
max_level = 11
coins_add = 0

white = (255, 255, 255)
blue = (0, 0, 255)

clock = pygame.time.Clock()
fps = 60

screen_width = 1450
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PLATFORMER")


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_grid():
    for line in range(0, tile_size + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


class Player:
    def __init__(self, x, y, image):
        self.reset(x, y, image)
        self.coins = coins

    def update(self, game_over):
        dx = 0
        dy = 0
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 7
                self.image = self.horse_left
            if key[pygame.K_RIGHT]:
                dx += 7
                self.image = self.player
            if key[pygame.K_SPACE] and not self.jumped:
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False

            # gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy = self.vel_y

            # collision
            for tile in world.tile_list:
                tile_img, tile_rect, tile_type = tile
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        if tile_type == 6:
                            if self.image == self.horse_left:
                                dx -= 15
                                for tile in world.tile_list:
                                    tile_img, tile_rect, tile_type = tile
                                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0

                                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        if self.vel_y < 0:
                                            dy = tile[1].bottom - self.rect.top
                                            self.vel_y = 0
                                        elif self.vel_y >= 0:
                                            dy = tile[1].top - self.rect.bottom
                                            self.vel_y = 0
                            else:
                                dx += 15
                                for tile in world.tile_list:
                                    tile_img, tile_rect, tile_type = tile
                                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0

                                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        if self.vel_y < 0:
                                            dy = tile[1].bottom - self.rect.top
                                            self.vel_y = 0
                                        elif self.vel_y >= 0:
                                            dy = tile[1].top - self.rect.bottom
                                            self.vel_y = 0
                        if tile_type == 5:
                            if self.image == self.horse_left:
                                dx -= 2
                                for tile in world.tile_list:
                                    tile_img, tile_rect, tile_type = tile
                                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0

                                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        if self.vel_y < 0:
                                            dy = tile[1].bottom - self.rect.top
                                            self.vel_y = 0
                                        elif self.vel_y >= 0:
                                            dy = tile[1].top - self.rect.bottom
                                            self.vel_y = 0
                            else:
                                dx += 2
                                for tile in world.tile_list:
                                    tile_img, tile_rect, tile_type = tile
                                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0

                                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        if self.vel_y < 0:
                                            dy = tile[1].bottom - self.rect.top
                                            self.vel_y = 0
                                        elif self.vel_y >= 0:
                                            dy = tile[1].top - self.rect.bottom
                                            self.vel_y = 0

            if self.fire:
                if pygame.sprite.spritecollide(self, lava_group, False):
                    game_over = -1
            if self.bear:
                if pygame.sprite.spritecollide(self, bear_group, False):
                    game_over = -1
            if not self.bear:
                pygame.sprite.spritecollide(self, bear_group, True)
            if pygame.sprite.spritecollide(self, flag_group, False):
                game_over = 1

            self.rect.x += dx
            self.rect.y += dy

        if game_over == -1:
            self.image = self.ghost

            self.rect.y -= 5
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y, image):
        self.player = image
        self.fire = True
        self.bear = True
        if image == dragon_p:
            self.player = pygame.transform.scale(self.player, (90, 49))
        if image == dragon_br:
            self.bear = False
        if image == dragon_w:
            self.player = pygame.transform.scale(self.player, (45, 45))
        else:
            self.player = pygame.transform.scale(self.player, (90, 61))
            if image == dragon_r:
                self.fire = False
        self.image = self.player
        self.horse_left = pygame.transform.flip(self.player, True, False)
        self.ghost = pygame.transform.scale(pygame.image.load("platformer stuff/ghost2.png"), (88, 112))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.jumped = False


class World:
    def __init__(self, data):
        self.tile_list = []
        rocks = pygame.image.load("platformer stuff/rocks.png")
        grass = pygame.image.load("platformer stuff/grass.png")
        sand = pygame.image.load("platformer stuff/sand.png")
        ice = pygame.image.load("platformer stuff/ice.png")
        flag = pygame.image.load("platformer stuff/flag.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect, tile)
                    self.tile_list.append(tile_info)
                if tile == 2:
                    img = pygame.transform.scale(rocks, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect, tile)
                    self.tile_list.append(tile_info)
                if tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                if tile == 4:
                    water = Water(col_count * tile_size, row_count * tile_size)
                    water_group.add(water)
                if tile == 5:
                    img = pygame.transform.scale(sand, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect, tile)
                    self.tile_list.append(tile_info)
                if tile == 6:
                    img = pygame.transform.scale(ice, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect, tile)
                    self.tile_list.append(tile_info)
                if tile == 7:
                    flag = Flag(col_count * tile_size, row_count * tile_size)
                    flag_group.add(flag)
                if tile == 8:
                    bear = Enemy(col_count * tile_size, row_count * tile_size - 20)
                    bear_group.add(bear)
                if tile == 9:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/bear.png"), (120, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.counter = 0

    def update(self):
        self.rect.x += self.direction
        self.counter += 1
        if self.counter > 150:
            self.direction *= -1
            self.counter = 0


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/lava.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/water.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/coin.png"),
                                            (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/flag.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def reset_level(level_index, image):
    player.reset(70, screen_height - 200, image)
    bear_group.empty()
    lava_group.empty()
    flag_group.empty()
    water_group.empty()
    coin_group.empty()
    world = World(world_data[level_index])
    return world


# sun = pygame.transform.scale(pygame.image.load("platformer stuff/sun no bg.png"), (70, 70))
sky = pygame.transform.scale(pygame.image.load("platformer stuff/new sky.png"), (screen_width, screen_height))
night = pygame.transform.scale(pygame.image.load("platformer stuff/night.png"), (screen_width, screen_height))
restart_img = pygame.transform.scale(pygame.image.load("platformer stuff/restart.png"), (200, 100))
exit_img = pygame.transform.scale(pygame.image.load("platformer stuff/exit.png"), (200, 100))
play_img = pygame.transform.scale(pygame.image.load("platformer stuff/play.png"), (200, 100))
shop_img = pygame.transform.scale(pygame.image.load("platformer stuff/shop.png"), (200, 100))
dragon_bl = pygame.image.load("platformer stuff/dragon blue.png")
dragon_r = pygame.image.load("platformer stuff/dragon red.png")
dragon_p = pygame.image.load("platformer stuff/dragon purple.png")
dragon_w = pygame.image.load("platformer stuff/dragon white2.png")
dragon_rain = pygame.image.load("platformer stuff/dragon rainbow.png")
dragon_g = pygame.image.load("platformer stuff/dragon green.png")
dragon_br = pygame.image.load("platformer stuff/dragon brown.png")
coin10 = pygame.transform.scale(pygame.image.load("platformer stuff/10.png"), (200, 100))
coin15 = pygame.transform.scale(pygame.image.load("platformer stuff/15.png"), (200, 100))
coin20 = pygame.transform.scale(pygame.image.load("platformer stuff/20.png"), (200, 100))
player_img = pygame.image.load("platformer stuff/dragon small.png")
img = pygame.image.load("platformer stuff/dragon small.png")

world_data = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 9, 2, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [2, 2, 2, 3, 3, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 1],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 1],
        [2, 0, 0, 0, 0, 0, 9, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [2, 2, 2, 6, 6, 6, 6, 4, 4, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 0, 0, 2, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 2, 0, 0, 0, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 9, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 8, 0, 0, 9, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 2, 5, 5, 5, 9, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1],
        [2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 9, 2, 2, 0, 9, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 1],
        [2, 2, 2, 2, 6, 6, 2, 0, 0, 0, 0, 2, 6, 0, 0, 0, 0, 2, 6, 6, 6, 2, 9, 0, 0, 0, 2, 2, 1],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 1],
        [2, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 1],
        [2, 0, 0, 0, 0, 0, 8, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1],
        [2, 2, 2, 6, 6, 6, 6, 4, 4, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 0, 9, 2, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ], [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 3, 3, 3, 2, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 5, 5, 5, 2, 0, 0, 2, 5, 5, 5, 0, 2, 0, 0, 2, 5, 5, 5, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 0, 0, 2, 0, 9, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 9, 0, 0, 0, 1],
        [1, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 9, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 1],
        [1, 2, 2, 4, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ], [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 0, 1],
        [1, 0, 6, 0, 0, 6, 0, 0, 0, 6, 0, 0, 7, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 1],
        [1, 0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 2, 3, 3, 0, 1],
        [1, 0, 2, 0, 0, 2, 0, 9, 2, 0, 0, 0, 0, 2, 0, 9, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1],
        [1, 0, 2, 5, 5, 2, 0, 0, 2, 5, 5, 5, 0, 2, 0, 0, 2, 5, 5, 5, 0, 2, 0, 0, 2, 0, 9, 0, 1],
        [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 9, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1],
        [1, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 9, 0, 2, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 6, 6, 6, 1],
        [1, 2, 2, 4, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 1],
        [1, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 1],
        [1, 0, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 0, 1],
        [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
        [1, 0, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 0, 1],
        [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 6, 6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 6, 6, 0, 6, 6, 1],
        [1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 6, 6, 6, 1],
        [1, 2, 2, 4, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 7, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 9, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 1],
        [1, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 1],
        [1, 0, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 0, 1],
        [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
        [1, 0, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 0, 1],
        [1, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 6, 6, 6, 0, 0, 0, 6, 6, 6, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 6, 6, 6, 1],
        [1, 2, 2, 4, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 0, 7, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 9, 0, 0, 0, 0, 9, 0, 1],
        [1, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 1],
        [1, 0, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 0, 1],
        [1, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 1],
        [1, 0, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 5, 2, 0, 1],
        [1, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 9, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 1],
        [1, 2, 2, 4, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 2, 2, 2, 4, 4, 2, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 7, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ],
    [
        [1] * 29,
        [1, 0, 0, 0, 0, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 1],
        [1, 3, 3, 3, 0, 2, 2, 2, 4, 4, 4, 0, 0, 2, 2, 0, 4, 4, 4, 0, 2, 2, 2, 2, 0, 0, 9, 0, 1],
        [1, 2, 2, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 7, 2, 0, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1],
        [1, 2, 5, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 9, 2, 0, 0, 0, 2, 0, 0, 0, 2, 5, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1]
    ], [
        [1] * 29,
        [1, 7, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1],
        [1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 9, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1, 4, 4, 4, 0, 2, 3, 2, 4, 4, 4, 0, 2, 3, 2, 0, 4, 4, 4, 0, 2, 3, 2, 4, 4, 4, 0, 0, 1],
        [1, 2, 5, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 5, 2, 9, 0, 0, 1],
        [1, 2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 1],
        [1, 2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 1],
        [1, 2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 1],
        [1, 2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 1],
        [1] + [0] * 27 + [9] + [1],
        [1] + [6] * 28 + [1],
        [1, 2, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1]
    ],
    [
        [1] * 29,
        [1] + [0] * 27 + [1],
        [1, 0, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 0, 0, 1],
        [1, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 0, 7, 1],
        [1, 0, 2, 4, 4, 4, 2, 4, 4, 4, 2, 4, 4, 4, 2, 4, 4, 4, 2, 4, 4, 4, 2, 4, 4, 4, 0, 0, 1],
        [1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
        [1] + [2] * 25 + [0] * 2 + [1],
        [1] + [0] * 27 + [1],
        [1] + [0] * 2 + [6] * 25 + [1],
        [1] + [0] * 27 + [1],
        [1] + [2] * 27 + [1],
        [1] * 29
    ],
    [
        [1] * 29,
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 0, 0, 1],
        [1, 0, 5, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 2, 0, 5, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 4, 4, 4, 0, 2, 0, 4, 4, 4, 0, 2, 0, 4, 4, 4, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1],
        [1] + [6] * 25 + [0, 0] + [1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
        [1] + [0] * 2 + [2] * 25 + [2] + [1],
        [1] + [0] * 27 + [0] + [1],
        [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
        [1, 0, 0] + [1] * 27,
        [0] * 29,
        [0] * 29,
        [1] * 2 + [0] * 27
    ]
]

restart = Button(1025, 350, restart_img)
exit_button = Button(225, 350, exit_img)
exit_button2 = Button(1200, 50, exit_img)
play = Button(1025, 350, play_img)
shop = Button(625, 350, shop_img)
dragon_purple = Button(100, 300, coin15)
dragon_blue = Button(450, 300, coin10)
dragon_red = Button(800, 300, coin10)
dragon_brown = Button(1150, 300, coin20)
dragon_green = Button(100, 600, coin10)
dragon_white = Button(450, 600, coin20)
dragon_rainbow = Button(800, 600, coin10)

bear_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
counting_coin = Coin(tile_size // 2, tile_size // 2)

player = Player(70, screen_height - 200, player_img)
world = World(world_data[level_index])

run = True

while run:

    clock.tick(fps)
    screen.blit(sky, (0, 0))
    # screen.blit(sun, (40, 40))
    if menu:
        if exit_button.draw():
            run = False
        if play.draw():
            menu = False
        if shop.draw():
            menu = False
            shop_screen = True
    elif shop_screen:
        draw_text((str(coins) + " + " + str(coins_add)), font_score, white, tile_size - 10, 10)
        screen.blit(pygame.transform.scale(dragon_p, (180, 122)), (110, 170))
        screen.blit(pygame.transform.scale(dragon_bl, (180, 122)), (460, 170))
        screen.blit(pygame.transform.scale(dragon_r, (180, 122)), (810, 170))
        screen.blit(pygame.transform.scale(dragon_br, (180, 122)), (1160, 170))
        screen.blit(pygame.transform.scale(dragon_g, (180, 122)), (110, 470))
        screen.blit(pygame.transform.scale(dragon_w, (180, 122)), (460, 470))
        screen.blit(pygame.transform.scale(dragon_rain, (180, 122)), (810, 470))

        if dragon_red.draw():
            if coins >= 10:
                coins -= 10
                player_img = dragon_r
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_blue.draw():
            if coins >= 10:
                coins -= 10
                player_img = dragon_bl
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_purple.draw():
            if coins >= 15:
                coins -= 15
                player_img = dragon_p
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_brown.draw():
            if coins >= 20:
                coins -= 20
                player_img = dragon_br
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_white.draw():
            if coins >= 20:
                coins -= 20
                player_img = dragon_w
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_rainbow.draw():
            if coins >= 10:
                coins -= 10
                player_img = dragon_rain
                game_over = 0
                player.reset(50, 600, player_img)

        if dragon_green.draw():
            if coins >= 10:
                coins -= 10
                player_img = dragon_g
                game_over = 0
                player.reset(50, 600, player_img)

        if exit_button2.draw():
            shop_screen = False
    else:
        world.draw()
        if game_over == 0:
            bear_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                coins_add += 1
            draw_text((str(coins) + " + " + str(coins_add)), font_score, white, tile_size - 10, 10)

        if game_over == -1:
            coins_add = 0
            player_img = img
            if restart.draw():
                world = []
                world = reset_level(level_index, player_img)
                game_over = 0
            if exit_button.draw():
                run = False
                coins = 0
            if shop.draw():
                menu = False
                shop_screen = True

        if next_level:
            if shop.draw():
                menu = False
                shop_screen = True

            if exit_button.draw():
                run = False
                coins = 0

            if play.draw():
                next_level = False

        if game_over == 1:
            menu = True
            level_index += 1
            if level_index <= max_level - 1:
                world = []
                world = reset_level(level_index, player_img)
                game_over = 0
                coins += coins_add
                coins_add = 0
            if shop.draw():
                menu = False
                shop_screen = True
            else:
                if restart.draw():
                    level_index = 0
                    world = reset_level(level_index, player_img)
                    game_over = 0
                    coins += coins_add
                if shop.draw():
                    menu = False
                    shop_screen = True
        bear_group.draw(screen)
        lava_group.draw(screen)
        flag_group.draw(screen)
        coin_group.draw(screen)
        water_group.draw(screen)

        game_over = player.update(game_over)
        # draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
