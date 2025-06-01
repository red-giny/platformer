import pygame
from pygame.locals import *

pygame.init()

font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

tile_size = 50
game_over = 0
menu = True
level_index = 0
max_level = 2
shop_screen = False
coins = 50
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
                self.image = self.horse
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
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, bear_group, False):
                game_over = -1
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
        self.player = pygame.transform.scale(self.player, (90, 61))
        self.image = self.player
        self.horse_left = pygame.transform.flip(self.player, True, False)
        self.ghost = pygame.transform.scale(pygame.image.load("platformer stuff/ghost2.png"), (88, 112))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False


class World:
    def __init__(self, data):
        self.tile_list = []
        rocks = pygame.image.load("platformer stuff/rocks.png")
        grass = pygame.image.load("platformer stuff/grass.png")
        water = pygame.image.load("platformer stuff/water.png")
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
                    tile_info = (img, img_rect)
                    self.tile_list.append(tile_info)
                if tile == 2:
                    img = pygame.transform.scale(rocks, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect)
                    self.tile_list.append(tile_info)
                if tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                if tile == 4:
                    img = pygame.transform.scale(water, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect)
                    self.tile_list.append(tile_info)
                if tile == 5:
                    img = pygame.transform.scale(sand, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect)
                    self.tile_list.append(tile_info)
                if tile == 6:
                    img = pygame.transform.scale(ice, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_info = (img, img_rect)
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


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/coin.png"), (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("platformer stuff/flag.png"), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def reset_level(level_index):
    player.reset(70, screen_height - 200)
    bear_group.empty()
    lava_group.empty()
    flag_group.empty()
    coin_group.empty()
    world = World(world_data[level_index])
    return world


sun = pygame.transform.scale(pygame.image.load("platformer stuff/sun no bg.png"), (70, 70))
cloud = pygame.transform.scale(pygame.image.load("platformer stuff/clouds.png"), (screen_width, screen_height))
restart_img = pygame.transform.scale(pygame.image.load("platformer stuff/restart.png"), (200, 100))
exit_img = pygame.transform.scale(pygame.image.load("platformer stuff/exit.png"), (200, 100))
play_img = pygame.transform.scale(pygame.image.load("platformer stuff/play.png"), (200, 100))
shop_img = pygame.transform.scale(pygame.image.load("platformer stuff/shop.png"), (200, 100))
dragon_b = pygame.transform.scale(pygame.image.load("platformer stuff/dragonblue.png"), (200, 100))
dragon_r = pygame.transform.scale(pygame.image.load("platformer stuff/dragonred.png"), (200, 100))
dragon_p = pygame.transform.scale(pygame.image.load("platformer stuff/dragonpurple.png"), (200, 100))
coin10 = pygame.transform.scale(pygame.image.load("platformer stuff/10.png"), (200, 100))
coin15 = pygame.transform.scale(pygame.image.load("platformer stuff/15.png"), (200, 100))
coin20 = pygame.transform.scale(pygame.image.load("platformer stuff/20.png"), (200, 100))
player_img = pygame.image.load("platformer stuff/dragon small.png")


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
    ]]

restart = Button(screen_width // 2 + 100, screen_height // 2, restart_img)
exit_button = Button(screen_width // 2 - 300, screen_height // 2 + 2, exit_img)
play = Button(screen_width // 2 + 100, screen_height // 2, play_img)
shop = Button(screen_width // 2 - 150, screen_height // 2, shop_img)
dragon_purple = Button(screen_width // 2 + 100, screen_height // 2, coin10)
dragon_blue = Button(screen_width // 2 - 150, screen_height // 2, coin10)
dragon_red = Button(screen_width // 2 - 350, screen_height // 2, coin10)


bear_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

player = Player(70, screen_height - 200, player_img)
world = World(world_data[level_index])

run = True

while run:

    clock.tick(fps)
    screen.blit(cloud, (0, 0))
    screen.blit(sun, (40, 40))
    if menu:
        if exit_button.draw():
            run = False
        if play.draw():
            menu = False
        if shop.draw():
            menu = False
            shop_screen = True
    elif shop_screen:
        if dragon_red.draw():
            if coins >= 10:
                coins -= 10
        if dragon_blue.draw():
            if coins >= 10:
                coins -= 10
        if dragon_purple.draw():
            if coins >= 10:
                coins -= 10
    else:
        world.draw()
        if game_over == 0:
            bear_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                coins_add += 1
            draw_text("X " + str(coins), font_score, white, tile_size - 10, 10)

        if game_over == -1:
            if restart.draw():
                world = []
                world = reset_level(level_index)
                game_over = 0
                coins_add = 0
            if exit_button.draw():
                run = False
                coins = 0
        if game_over == 1:
            level_index += 1
            if level_index <= max_level - 1:
                world = []
                world = reset_level(level_index)
                game_over = 0
                coins += coins_add
            else:
                if restart.draw():
                    level_index = 0
                    world = reset_level(level_index)
                    game_over = 0
                    coins += coins_add
        bear_group.draw(screen)
        lava_group.draw(screen)
        flag_group.draw(screen)
        coin_group.draw(screen)

        game_over = player.update(game_over)
        # draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

qwerty
