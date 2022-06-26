import pathlib

# WINDOW Settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Velkommen til Neste Planet"

# character 
PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 20
HIT_JUMP = 5
GRAVITY = 1
PLAYER_START_X = 500
PLAYER_START_Y = 250

#Sprites
CHARACTER_SCALING = 3
TILE_SCALING = 2
MANA_SCALING = 8
ENEMY_SCALING = 3
ENEMY_SPRITE_ADJUSTMENT_Y = 24

SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING


# Layer Names from TileMap
LAYER_NAME_GROUND = "ground"
LAYER_NAME_OBJECTS = "items"
LAYER_NAME_FOREGROUND = "foreground"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_DONT_TOUCH = "donttouch"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_MANA = "Mana"