import pygame as pg
from math import floor

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
FPS = 30

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player Settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
MOB_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)

class Cooldown:
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0

    def ticking(self):
        self.current_time = floor(pg.time.get_ticks()/1000)
        self.delta = self.current_time - self.event_time

    def timer(self):
        self.current_time = floor(pg.time.get_ticks()/1000)