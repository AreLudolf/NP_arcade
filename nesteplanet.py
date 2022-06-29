import arcade
import playerchar
import settings
import enemies
import manaHUD
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
        self.manahud_sprite = None
        self.hphud_sprite = None
        self.hp = 3
        self.tile_map = None
        self.end_of_map = 0
        self.level = 1
        self.enemies_layer = None
        self.manahud_sprite_list = None
        self.can_shoot = False
        self.shoot_timer = 0


        arcade.set_background_color(arcade.csscolor.THISTLE)

        
        # Load sounds
        self.collect_mana_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")


    def setup(self):
        """game setup or restart"""

        # Set up the Camera and GUI-camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.reset_hp = True
        self.reset_mana = True
        self.manahud_sprite_list = arcade.SpriteList()

        # Load tiledmap
        map_name = os.path.join(os.path.dirname(__file__),  "assets", "level_01.tmj")
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
            },
            settings.LAYER_NAME_MANA: {
                "use_spatial_hash": True
            },
            settings.LAYER_NAME_SIGN: {
                "use_spatial_hash": True
            },
            settings.LAYER_NAME_SIGNTEXT: {
                "use_spatial_hash": True
            }

        }
        self.tile_map = arcade.load_tilemap(map_name, settings.TILE_SCALING, layer_options)


        # Init arcade scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)        
        self.scene.add_sprite_list_after("Player", settings.LAYER_NAME_FOREGROUND)

        # Set up the player, spawn at coordinates
        self.player_sprite = playerchar.PlayerCharacter()
        self.player_sprite.center_x = settings.PLAYER_START_X
        self.player_sprite.center_y = settings.PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Background from tiled?
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=settings.GRAVITY, walls=self.scene["ground"]
        )

        # Calculate end of map for level cleared.
        self.end_of_map = self.tile_map.width * settings.GRID_PIXEL_SIZE

        # -- ENEMIES setup
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
            
            # Does enemy move? Move properties set in map
            if "change_x" in en.properties:
                enemy.change_x = en.properties["change_x"]
            if "boundary_left" in en.properties:
                enemy.boundary_left = en.properties["boundary_left"]
            if "boundary_right" in en.properties:
                enemy.boundary_right = en.properties["boundary_right"]

            self.scene.add_sprite(settings.LAYER_NAME_ENEMY, enemy)

        # Not sure if this works
        self.physics_engine_enemies = arcade.PhysicsEnginePlatformer(
            self.scene[settings.LAYER_NAME_ENEMY], gravity_constant=settings.GRAVITY, walls=self.scene["ground"]
        )

        # Sign text popup setup
        self.signtext_layer = self.tile_map.sprite_lists[settings.LAYER_NAME_SIGNTEXT]
        print(self.signtext_layer)
        for text in self.signtext_layer:
            print(text)
            text.alpha = 0


        # Mana count on HUD. HUD items as separate file and class?
        self.manahud_list = arcade.SpriteList(use_spatial_hash=True)

        mana_img = main_path = os.path.join(os.path.dirname(__file__), "assets", "img", "items", "mana.png")
        self.manahud_pos = 30
        for mana in range(self.mana):
            self.manahud_sprite = arcade.Sprite(mana_img, settings.MANA_HUD_SCALING)
            self.manahud_sprite.center_x = self.manahud_pos
            self.manahud_pos += self.manahud_sprite.width
            self.manahud_sprite.center_y = 60
            self.manahud_list.append(self.manahud_sprite)

        # HP count on HUD
        self.hp_sprite_list = arcade.SpriteList(use_spatial_hash=True)

        hp_img = main_path = os.path.join(os.path.dirname(__file__),   "assets", "img", "items", "hp.png")
        self.hphud_pos = 30
        for mana in range(self.hp):
            self.hphud_sprite = arcade.Sprite(hp_img, settings.HP_HUD_SCALING)
            self.hphud_sprite.center_x = self.hphud_pos
            self.hphud_pos += self.hphud_sprite.width
            self.hphud_sprite.center_y = 30
            self.hp_sprite_list.append(self.hphud_sprite)



    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Draw sprites
        self.camera.use()
        self.scene.draw()


        # Draw HUD
        self.gui_camera.use()
        self.manahud_list.draw()
        self.hp_sprite_list.draw()

    

    def process_keychange(self):
        """
        Key up or down
        UP changed to spacebar. FIX: set controls in settings.py
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
            # FIX: Only 1 attack pr. keypress
            if self.mana > 0:
                self.player_sprite.attack()
                self.manahud_list[self.mana-1].center_y = -100

            else:
                print("Out of mana")

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

        if self.can_shoot:
            # FIX: Cannot shoot with mana = 1?
            if self.ctrl_pressed and self.mana > 0:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    settings.SPRITE_SCALING_BULLET,
                )
                self.mana -= 1

                if self.player_sprite.character_face_direction == playerchar.RIGHT_FACING:
                    bullet.change_x = settings.BULLET_SPEED
                else:
                    bullet.change_x = -settings.BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(settings.LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == settings.SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0


        # Update anumations
        self.scene.update_animation(
            delta_time, [settings.LAYER_NAME_OBJECTS, settings.LAYER_NAME_BACKGROUND, "Player", settings.LAYER_NAME_ENEMY]
        )

        # Update enemy if moving
        self.scene.update([settings.LAYER_NAME_ENEMY, settings.LAYER_NAME_BULLETS])

        # Check enemy collision with boundary set in Tiledmap
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

        # Bullet collision check
        for bullet in self.scene[settings.LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[settings.LAYER_NAME_ENEMY],
                    self.scene[settings.LAYER_NAME_GROUND],
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if (
                        self.scene[settings.LAYER_NAME_ENEMY]
                        in collision.sprite_lists
                    ):
                        # The collision was with an enemy
                        collision.health -= settings.BULLET_DAMAGE

                        if collision.health <= 0:
                            collision.remove_from_sprite_lists()

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * settings.TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()


        # Check mana pickup
        mana_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Mana"])
        
        for mana in mana_hit_list:
            # Add 1 mana
            if self.mana < 3:
                mana.remove_from_sprite_lists()
                arcade.play_sound(self.collect_mana_sound)
                self.manahud_list[self.mana].center_y = +60
                self.mana += 1
            else:
                pass
            
        
        # Player hit enemy, ouch!
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[settings.LAYER_NAME_ENEMY])
        for enemy in enemy_hit_list:
            # FIX: IF NO KEY IS PRESSED, CHANGE_X KEEPS MOVING CHARACTER
            # FIX: Currently take several HP from one enemy attack.
            self.hp_sprite_list[self.hp-1].center_y = -100
            self.hp -= 1
            #Cancel all movement and actions
            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False
            self.jump_needs_reset = False
            self.ctrl_pressed = False

            self.player_sprite.change_y = settings.HIT_JUMP
            # What side is the attack coming from?
            if self.player_sprite.center_x - enemy.center_x < 0:
                self.player_sprite.change_x = -settings.HIT_JUMP

            if self.player_sprite.center_x - enemy.center_x > 0:
                self.player_sprite.change_x = settings.HIT_JUMP

        # Sign hit?
        sign_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[settings.LAYER_NAME_SIGN])

        if sign_hit_list:
            for text in self.signtext_layer:
                print(text)
                text.alpha = 255
        else:
            for text in self.signtext_layer:
                text.alpha = 0
        
        # KOMMENTAR TIL BENDIK HALLO GIT ER KULT
        # GIROIJSOFØIJOSØIJE

        # Position camera
        self.center_camera_to_player()

        # Fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = settings.PLAYER_START_X
            self.player_sprite.center_y = settings.PLAYER_START_Y

            arcade.play_sound(self.game_over)

        """
        DONT TOUCH!? Layer from tilemap with traps etc. Currently starts over, change to lose HP
        """
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[settings.LAYER_NAME_DONT_TOUCH]
        ):
            # Respawn at start
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = settings.PLAYER_START_X
            self.player_sprite.center_y = settings.PLAYER_START_Y

            arcade.play_sound(self.game_over)

        # If end of map, next level(change to door or similar).
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            print("END OF MAP: " + self.end_of_map)

            # Keep MANA and HP

            self.reset_mana = False

            self.setup()
