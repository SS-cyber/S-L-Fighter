import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "FILLERNAME"

CHARACTER_SCALING = 1.25
TILE_SCALING = 0.5


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.player_list = None

        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite("Sprites\Player\player_0.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        # Code to draw the screen goes here
        self.wall_list.draw()
        self.player_list.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
