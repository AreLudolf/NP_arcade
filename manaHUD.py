import arcade
import math
import settings
import os

class manahud(arcade.Sprite):
    """
    Mana on HUD display class
    """

    def __init__(self, mana_count):
        """ Initialize mana display """
        self.mana_count = mana_count
        main_path = os.path.join(os.path.abspath(__file__), "..", "assets", "img", "items", "mana")
        self.screen_width = settings.SCREEN_WIDTH
        self.screen_height = settings.SCREEN_HEIGHT
        self.manahud_scaling = settings.MANA_HUD_SCALING
        self.mana_sprite = arcade.load_texture(f"{main_path}.png")

        
        super().__init__()
        
        # Automatically position mana count image based on the number of mana count
        self.center_x = self.screen_width * 0.1
        self.center_y = (self.screen_height * 0.1 ) + (self.mana_count*self.screen_height*0.03)