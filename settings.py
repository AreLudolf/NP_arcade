import pathlib

# WINDOW Settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Velkommen til Neste Planet"

# character 
PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 20
HIT_JUMP = 10
GRAVITY = 1
PLAYER_START_X = 500
PLAYER_START_Y = 250

# Sprites
CHARACTER_SCALING = 3
TILE_SCALING = 2
MANA_SCALING = 10
MANA_HUD_SCALING = 2
HP_HUD_SCALING = 1
ENEMY_SCALING = 3
ENEMY_SPRITE_ADJUSTMENT_Y = 24
SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Attack
SPRITE_SCALING_BULLET = 0.8
SHOOT_SPEED = 20
BULLET_SPEED = 12
BULLET_DAMAGE = 25


# Layer Names from TileMap
LAYER_NAME_GROUND = "ground"
LAYER_NAME_OBJECTS = "items"
LAYER_NAME_FOREGROUND = "foreground"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_DONT_TOUCH = "donttouch"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_MANA = "Mana"
LAYER_NAME_SIGN = "signs"
LAYER_NAME_BULLETS = "bullets"
LAYER_NAME_SIGNTEXT = "signtext"