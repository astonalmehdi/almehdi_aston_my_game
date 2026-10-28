# This file was created by: Aston
# Content inspiered by: Chris Cozort
# I do solemnly swear to create concise and informative comments

'''
The game engin consists of three (four) basic components:
Input - keys, buttons, voice, mouse, touch, movement, joystick
Process - input processed (direction of control, magnitude)
Output - draw new frames, sound, haptics
(Store)

GOALS:
RULES:
FEEDBACK:
FREEDOM:
'''

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *

# Blueprint for the whole game
class Game:
    def __init__(self):
        # Initializes the attributes needed for the game, screen and clock
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
        self.game_save_dir = path.join(self.game_dir, "highscore.txt")
        self.img_dir = path.join(self.game_dir, "images")
        self.snd_dir = path.join(self.game_dir, "sounds")
        self.map = Map(path.join(self.game_dir, map))

        try:
            with open(self.game_save_dir, "x", encoding = "utf-8") as file:
                file.write("Hello World!")
            print("File created")
        except FileExistsError:
            print("File already exists. No action take.")

        with open(self.game_save_dir, "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                print("Highscore is 0!")

    def new(self):
        # Creates the map, including the player
        self.load_data("level1.txt")
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row, self.all_coins)
                if tile == "M":
                    Mob(self, col, row)
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "C":
                    Coin(self, col, row)

        pg.mixer.music.load(path.join(self.snd_dir, "background_music.ogg"))
        pg.mixer.music.play(loops = -1)

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
                if self.player.score > self.highscore:
                    with open(path.join(self.game_dir, self.game_save_dir), "w") as f:
                        f.write(str(self.player.score))
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # This block of code handles processing of changes based on input
        self.all_sprites.update()

    def draw_text(self, text, size, color, x, y):
        # Draw text on screen anywhere
        font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        # Draws all the sprites
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames per second: " + str(floor(1/self.dt)), 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(f"Coins: {self.player.score}", 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(f"Highscore: {self.highscore}", 24, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()