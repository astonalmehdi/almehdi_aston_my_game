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
PLAYER_FRIC = -0.2
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
MOB_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)