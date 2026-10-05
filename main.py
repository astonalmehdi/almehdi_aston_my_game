# This file was created by: Aston
# Content inspiered by: Chris Cozort
# I do solemnly swear to create concise and informative comments

'''
The game engin consists of three (four) basic components:
Input - keys, buttons, voice, mouse, touch, movement, joystick
Process - input processed (direction of control, magnitude)
Output - draw new frames, sound, haptics
(Store)
'''

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *

# Blueprint for the whole game
class Game:
    def __init__(self):
        # Initializes the attributes needed for the game. Screen and clock
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game class initialized")
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True

    def load_data(self, map):
        # Loads all the sprites and sounds(don't have any yet)
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, "images")
        self.snd_dir = path.join(self.game_dir, "sounds")
        self.map = Map(path.join(self.game_dir, map))

    def new(self):
        # Creates the map, including the player
        self.load_data("level1.txt")
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)

    def run(self):
        # Keeps the game running
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events() # Gets player input
            self.update() # Updates the game
            self.draw() # Draws sprites
    
    def events(self):
        # Checks if we want to exit the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.player.pos = event.pos

    def update(self):
        # This block of code handles processing of changes based on input
        self.all_sprites.update()
    
    def draw(self):
        # Draws all the sprites
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()