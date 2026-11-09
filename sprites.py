import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from random import uniform, choice

vec = pg.math.Vector2

def collide_hit_rect(one, two):
    # Checks if two objects are colliding
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    # Checks if the object is colliding with walls
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if dir == "x":
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
            
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height/2
        
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y, coins):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        # Necesary attributes needed for player
        self.game = game
        self.coins = coins
        self.score = 0
        # Gives us coin sound
        self.coin_pickup = pg.mixer.Sound("sounds/coin.wav")
        # this provides us with raster images for use in animation or otherwise
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # player motion attributes
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.player_fric = -0.1
        self.hit_rect = PLAYER_HIT_RECT
        # animation stuff
        self.current_frame = 0
        self.last_update = 0
        # accounting for the states of the player
        self.jumping = False # Haven't added jump yet
        self.moving = False
        self.load_images()
        print("player instance created")

    def get_keys(self):
        # Checks if any keys are being pressed to move the player
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC

    def jump(self):
        pass

    def load_images(self):
        # Loads sprites for player
        # self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]
        # self.moving_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]
        self.idle_frames = [pg.image.load(path.join(self.game.img_dir, "tarun venkat.jpg"))]
        self.moving_frames = [pg.image.load(path.join(self.game.img_dir, "tarun venkat.jpg"))]

    def animate(self):
        # If their are multiple sprites then it will go through them
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                # self.image.set_colorkey(BLACK)
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.image.set_colorkey(BLACK)

    def check_coins(self):
        # Sees if the player collided with coins
        hits = pg.sprite.spritecollide(self, self.coins, True)
        self.score += len(hits)
        if hits:
            # Plays coin pickup sound and creates particles
            self.coin_pickup.play()
            for i in range(0, 10):
                Particle(self.game, self.rect.x, self.rect.y)

    def update(self):
        self.animate()
        self.acc = vec(0, 0)
        self.get_keys()
        self.acc.x += self.vel.x * self.player_fric
        self.acc.y += self.vel.y * self.player_fric
        self.vel += self.acc
        self.rect.center = self.pos
        # self.pos += self.vel * self.game.dt
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        self.pos += self.vel * self.game.dt + 0.5 * self.acc
        
        tile_hits = pg.sprite.spritecollide(self, self.game.all_tiles, False)
        if tile_hits:
            if tile_hits[0].variant == "ice":
                self.player_fric = -0.01
            else:
                self.player_fric = -0.1
        
        self.check_coins()
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center

# copied player class
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # this provides us with raster images for use in animation or otherwise
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(64, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Movement stuff
        self.speed = 100
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = MOB_HIT_RECT
        # animation stuff
        self.current_frame = 0
        self.last_update = 0
        # accounting for the states of the player
        self.jumping = False
        self.moving = False
        self.load_images()
        print("player instance created")

    def jump(self):
        pass

    def follow(self, obj):
        # figures out what direction they need to go to follow the player
        direction = vec(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        self.vel = direction

    def load_images(self):
        # Loads the sprites for the mob
        self.idle_frames = [self.spritesheet.get_image(64,0, TILESIZE,TILESIZE), self.spritesheet.get_image(96,0, TILESIZE,TILESIZE)]
        self.moving_frames = [self.spritesheet.get_image(64,0, TILESIZE,TILESIZE), self.spritesheet.get_image(96,0, TILESIZE,TILESIZE)]

    def animate(self):
        # If their are multiple sprites then it will go through them
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.image.set_colorkey(BLACK)
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.image.set_colorkey(BLACK)

    def update(self):
        self.animate()
        self.follow(self.game.player)
        self.pos += self.vel * self.speed * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center

# Copied from wall
class Particle(Sprite):
    def __init__(self, game, x, y):
        # Creates particle attributes
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        # Size and color
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Chooses a random direction to go
        self.vel = vec(uniform(-1, 1), uniform(-1, 1)) * 15
        self.pos = vec(x, y)
        self.rect.center = self.pos
        # Sets a countdown so that the particles can disappear after a little
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        print("Particle instance created")

    def update(self):
        # Countsdown till a certain time
        self.countdown.ticking()
        # Changes color to make them rainbow
        self.image.fill(choice([RED, GREEN, BLUE, YELLOW]))
        # Moving particle
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.countdown.delta > 1:
            self.kill()

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")

# Copied from wall class
class Surface(Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites, game.all_tiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")

# Copied from wall class
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, YELLOW, (TILESIZE/2, TILESIZE/2), TILESIZE/2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")