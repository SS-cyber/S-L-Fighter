import arcade
import math
import os

# Constants
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "FILLERNAME"

CHARACTER_SCALING = 1.25
TILE_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 4.5

TOP_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 50

GRID_PIXEL_SIZE = 64

BULLET_SPEED = 1

START_X = 576
START_Y = 128

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.player_list = None
        self.bullet_list = None
        self.thunder_list = None
        self.player_bullet_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_bottom = 0

        self.frame_count = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.plane_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list = arcade.SpriteList()
        self.thunder_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_bullet_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Sprites\Player\player_0.png", CHARACTER_SCALING)
        self.player_sprite.center_x = START_X
        self.player_sprite.center_y = START_Y
        self.player_list.append(self.player_sprite)
        map_name = "Maps\Test_Map.tmx"
        wall_layer_name = "CloudWall"
        enemy_layer_name = "EnemyPlane"
        thunder_layer_name = "ThunderCloud"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map, layer_name=wall_layer_name,
                                                      scaling=TILE_SCALING * 2.25, use_spatial_hash=True)
        self.plane_list = arcade.tilemap.process_layer(my_map, enemy_layer_name, TILE_SCALING * 2.25)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.thunder_list = arcade.tilemap.process_layer(map_object=my_map, layer_name=thunder_layer_name,
                                                         scaling=TILE_SCALING * 2.25, use_spatial_hash=True)

    def on_draw(self):
        arcade.start_render()
        # Code to draw the screen goes here
        self.wall_list.draw()
        self.player_list.draw()
        self.plane_list.draw()
        self.bullet_list.draw()
        self.thunder_list.draw()
        self.player_bullet_list.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        player_bullet = arcade.Sprite("Sprites\Player Bullet\Player_Bullet.png")
        player_bullet.change_y = BULLET_SPEED
        player_bullet.center_x = self.player_sprite.center_x
        player_bullet.bottom = self.player_sprite.top
        self.player_bullet_list.append(player_bullet)

    def on_update(self, delta_time):
        self.frame_count += 1
        self.physics_engine.update()
        changed = False

        if arcade.check_for_collision_with_list(self.player_sprite, self.thunder_list) or arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = START_X
            self.player_sprite.center_y = START_Y
            self.view_bottom = 0
            changed = True


        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

        for enemy in self.plane_list:
            start_x = enemy.center_x
            start_y = enemy.center_y
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            if math.sqrt((x_diff * x_diff) + (y_diff * y_diff)) < 600:
                angle = math.atan2(y_diff, x_diff)

                enemy.angle = math.degrees(angle) + 90

                if self.frame_count % 60 == 0:
                    bullet = arcade.Sprite("Sprites\Bullet\Bullet.png")
                    bullet.center_x = start_x
                    bullet.center_y = start_y
                    bullet.angle = math.degrees(angle) - 90
                    bullet.change_x = math.cos(angle) * BULLET_SPEED
                    bullet.change_y = math.sin(angle) * BULLET_SPEED
                    self.bullet_list.append(bullet)

            for bullet in self.bullet_list:
                if math.sqrt(((self.player_sprite.center_x - bullet.center_x) * (
                        self.player_sprite.center_x - bullet.center_x)) + (
                                     (self.player_sprite.center_y - bullet.center_y) * (
                                     self.player_sprite.center_y - bullet.center_y))) > 800:
                    bullet.remove_from_sprite_lists()

            self.bullet_list.update()

            self.player_bullet_list.update()
            for player_bullet in self.player_bullet_list:
                hit_list = arcade.check_for_collision_with_list(player_bullet, self.plane_list)
                if len(hit_list) > 0:
                    player_bullet.remove_from_sprite_lists()

                for plane in hit_list:
                    plane.remove_from_sprite_lists()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()