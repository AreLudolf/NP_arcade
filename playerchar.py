import arcade
import settings
import os


RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = settings.CHARACTER_SCALING

        # Track our state
        self.jumping = False

        # --- Load Textures ---
        #main_path = "assets/img/player/char"
        main_path = os.path.join(os.path.abspath(__file__), "..", "assets", "img", "player", "char")

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.gif")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.gif")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.gif")

        # Load textures for walking
        self.run_textures = []
        for i in range(6):
            texture = load_texture_pair(f"{main_path}_run_{i}.png")
            self.run_textures.append(texture)

        """
        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)
        """
        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 5:
            self.cur_texture = 0
        self.texture = self.run_textures[self.cur_texture][
            self.character_face_direction
        ]

    def attack(self):
        print("ATTACK!!")