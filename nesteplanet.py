import arcade
import playerchar
import settings
import enemies
import os
import math

class NestePlanet(arcade.Window):
    """
    Main game class.
    """

    def __init__(self):

        # setup arcade window
        super().__init__(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.ctrl_pressed = False

        # Init variables
        self.scene = None
        #self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.mana = 3
        self.hp = 3
        self.tile_map = None
        self.end_of_map = 0
        self.level = 1
        self.enemies_layer = None


        arcade.set_background_color(arcade.csscolor.THISTLE)

        
        # Load sounds
        self.collect_mana_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")


    def setup(self):
        """game setup or restart"""

        # Set up the Camera and GUI-camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.reset_hp = True
        self.reset_mana = True

        map_name = os.path.join(os.path.abspath(__file__), "..", "assets", "level_01.tmj")
        #map_name = "assets/level_01.tmj"

        layer_options = {
            settings.LAYER_NAME_GROUND: {
                "use_spatial_hash": True,
            },
            settings.LAYER_NAME_OBJECTS: {
                "use_spatial_hash": True,
            },
            settings.LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
            settings.LAYER_NAME_OBJECTS: {
                "use_spatial_hash": True,
            }
        }
        self.tile_map = arcade.load_tilemap(map_name, settings.TILE_SCALING, layer_options)


        # Init scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        
        self.scene.add_sprite_list_after("Player", settings.LAYER_NAME_FOREGROUND)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = playerchar.PlayerCharacter()
        self.player_sprite.center_x = settings.PLAYER_START_X
        self.player_sprite.center_y = settings.PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=settings.GRAVITY, walls=self.scene["ground"]
        )

        self.end_of_map = self.tile_map.width * settings.GRID_PIXEL_SIZE

        # -- ENEMIES
        self.enemies_layer = self.tile_map.object_lists[settings.LAYER_NAME_ENEMY]

        for en in self.enemies_layer:
            cartesian = self.tile_map.get_cartesian(en.shape[0], en.shape[1])
            enemy_type = en.properties["type"]
            if enemy_type == "robot":
                enemy = enemies.RobotEnemy()
            elif enemy_type == "zombie":
                enemy = enemies.ZombieEnemy()
            else:
                raise Exception(f"Unknown enemy type {enemy_type}.")
            enemy.center_x = math.floor(cartesian[0] * settings.TILE_SCALING *self.tile_map.tile_width)
            enemy.center_y = math.floor(cartesian[1] + 1) * (self.tile_map.tile_height * settings.TILE_SCALING) + settings.ENEMY_SPRITE_ADJUSTMENT_Y
            
            # Does enemy move?
            if "change_x" in en.properties:
                enemy.change_x = en.properties["change_x"]
            if "boundary_left" in en.properties:
                enemy.boundary_left = en.properties["boundary_left"]
            if "boundary_right" in en.properties:
                enemy.boundary_right = en.properties["boundary_right"]

            self.scene.add_sprite(settings.LAYER_NAME_ENEMY, enemy)

        self.physics_engine_enemies = arcade.PhysicsEnginePlatformer(
            self.scene[settings.LAYER_NAME_ENEMY], gravity_constant=settings.GRAVITY, walls=self.scene["ground"]
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        self.camera.use()
        # Draw sprites
        self.scene.draw()

        
        self.gui_camera.use()
        mana_text = f"mana: {self.mana}"
        arcade.draw_text(
            mana_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18
        )
        hp_text = f"HP: {self.hp}"
        arcade.draw_text(
            hp_text,
            10,
            30,
            arcade.csscolor.WHITE,
            18
        )
    

    def process_keychange(self):
        """
        Key up or down
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = settings.PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = settings.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -settings.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

        # Process attack
        if self.ctrl_pressed:
            self.player_sprite.attack()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""


        if key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LCTRL:
            self.ctrl_pressed = True
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LCTRL:
            self.ctrl_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        self.scene.update_animation(
            delta_time, [settings.LAYER_NAME_OBJECTS, settings.LAYER_NAME_BACKGROUND, "Player", settings.LAYER_NAME_ENEMY]
        )

        # Update enemy if moving
        self.scene.update([settings.LAYER_NAME_ENEMY])

        # Check collision with boundary set in Tiledmap
        for enemy in self.scene[settings.LAYER_NAME_ENEMY]:
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1


        # Check mana pickup
        mana_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Mana"])
        for mana in mana_hit_list:
            mana.remove_from_sprite_lists()
            arcade.play_sound(self.collect_mana_sound)
            # Add 1 mana
            self.mana += 1
        
        # Enemy hit, ouch!
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[settings.LAYER_NAME_ENEMY])
        for enemy in enemy_hit_list:
            self.hp -= 1
            self.player_sprite.change_y = settings.HIT_JUMP
            


        # Position camera
        self.center_camera_to_player()

        # Fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = settings.PLAYER_START_X
            self.player_sprite.center_y = settings.PLAYER_START_Y

            arcade.play_sound(self.game_over)

        # DONT TOUCH!?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[settings.LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = settings.PLAYER_START_X
            self.player_sprite.center_y = settings.PLAYER_START_Y

            arcade.play_sound(self.game_over)

        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            print("END OF MAP: " + self.end_of_map)

            # Keep MANA and HP

            self.reset_mana = False

            self.setup()
