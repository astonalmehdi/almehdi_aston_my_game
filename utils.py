import pygame as pg
from settings import *
from math import floor
from pygame.math import Vector2 as vector

class AllSprites(pg.sprite.Group):
    def __init__(self):
        pg.sprite.Group.__init__(self)
        self.display_surface = pg.display.get_surface()
        self.offset = vector()

    def custom_draw(self, player):
        # Offset Vector
        self.offset.x = player.rect.centerx - WIDTH/2
        self.offset.y = player.rect.centery - HEIGHT/2

        # Blit all sprites
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

# Makes a map
class Map:
    def __init__(self, filename):
        # Creates all the tiles
        self.data = []

        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tileheight * TILESIZE
        self.height = self.tileheight * TILESIZE
        print("map instantiated...")

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Makes an image with all of the sprites
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

class Cooldown:
    # Makes a timer
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0

    def ticking(self):
        # gets current time and gets the delta between that and the time that the event happened
        self.current_time = floor(pg.time.get_ticks()/1000)
        self.delta = self.current_time - self.event_time

    def timer(self):
        # gets new current time
        self.current_time = floor(pg.time.get_ticks()/1000)