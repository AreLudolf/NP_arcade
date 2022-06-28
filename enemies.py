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

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = settings.ENEMY_SCALING
        self.character_face_direction = RIGHT_FACING

        #main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        main_path = os.path.join(os.path.abspath(__file__), "..", "assets", "img", "enemies", "enemy")

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(6):
            texture = load_texture_pair(f"{main_path}_run_{i}.png")
            self.walk_textures.append(texture)


        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # OBS! Hit box will be set based on the first image used. 
        self.hit_box = self.texture.hit_box_points




class Enemy(Entity):
    def __init__(self, name_folder, name_file):

        # Setup parent class
        super().__init__(name_folder, name_file)
        self.should_update_walk = 0


    def update_animation(self, delta_time: float = 1/60):

        # Left or right facing
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return
        
        # Falling animation
        if self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 5:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1



class RobotEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("robot", "robot")


class ZombieEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("zombie", "zombie")