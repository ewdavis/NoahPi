"""
Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
The sprite_move_keyboard_better.py example is slightly better
in how it works, but also slightly more complex.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard
"""

import arcade
import random

SPRITE_SCALING = 2.0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ghosts!"

MOVEMENT_SPEED = 5

class Tree(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.sprite_sheet = "sprites/nature.png"
        self.sheet_x = 12
        self.sheet_y = 10
        self.texture = arcade.load_texture(self.sprite_sheet,
                                               x = self.sheet_x*16,
                                               y = self.sheet_y*16,
                                               width=16,
                                               height=16)
        self.scale = 2.0

class Spirit(arcade.Sprite):

    def __init__(self):
        super().__init__()
        i = 0
        j = 0
        self.monster_sprite = "sprites/snake_green.png"
        self.texture = arcade.load_texture(self.monster_sprite,
                                               x=i*16,
                                               y=j*16,
                                               width=16,
                                               height=16)
        self.my_speed = 0.5
        self.scale = 2.0

        self.SOUTH = 0
        self.NORTH = 1
        self.EAST = 2
        self.WEST = 3
        self.facing = self.SOUTH
        self.frame = 0
        self.frame_max = 4
        self.frame_delay = 4
        self.frame_buffer = 0
        self.x_change = 0
        self.y_change = 0

    def follow_sprite(self, player_sprite):

        self.x_change = (self.center_x - player_sprite.center_x)
        self.y_change = (self.center_y - player_sprite.center_y)

        if abs(self.x_change) > abs(self.y_change):
            if (self.x_change > 0):
                self.facing = self.EAST
            else:
                self.facing = self.WEST
        else:
            if (self.y_change > 0):
                self.facing = self.SOUTH
            else:
                self.facing = self.NORTH

        self.frame_buffer = self.frame_buffer + 1
        if (self.frame_buffer >= self.frame_delay):
            self.frame_buffer = 0
            self.frame = self.frame + 1
        
        if (self.frame >= self.frame_max):
            self.frame = 0

        self.texture = arcade.load_texture(self.monster_sprite,
                                               x=self.facing*16,
                                               y=self.frame*16,
                                               width=16,
                                               height=16)
            
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.my_speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.my_speed, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.my_speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.my_speed, self.center_x - player_sprite.center_x)

class Player(arcade.Sprite):

    """ Player Class """
    def __init__(self):
        super().__init__()
        i = 0
        j = 0
        self.player_sprite = "sprites/dark_ninja.png"
        self.player_sprite = "sprites/racoon.png"        
        self.texture = arcade.load_texture(self.player_sprite,
                                               x=i*16,
                                               y=j*16,
                                               width=16,
                                               height=16)
        self.scale = 2.0
        #self.sound = arcade.Sound("sprites/castle.wav")
        #self.sound.play(speed=1.0, volume=0.25)

        self.SOUTH = 0
        self.NORTH = 1
        self.EAST = 2
        self.WEST = 3
        self.facing = self.SOUTH
        self.frame = 0
        self.frame_max = 4
        self.frame_delay = 4
        self.frame_buffer = 0
        self.x_change = 0
        self.y_change = 0


    def update(self):

        """ Move the player """

        # Move player.

        # Remove these lines if physics engine is moving player.

        if (self.change_x != 0) or (self.change_y != 0):
            if abs(self.change_x) > abs(self.change_y):
                if (self.change_x > 0):
                    self.facing = self.WEST
                else:
                    self.facing = self.EAST
            else:
                if (self.change_y > 0):
                    self.facing = self.NORTH
                else:
                    self.facing = self.SOUTH

            self.frame_buffer = self.frame_buffer + 1
            if (self.frame_buffer >= self.frame_delay):
                self.frame_buffer = 0
                self.frame = self.frame + 1
        
                if (self.frame >= self.frame_max):
                    self.frame = 0

        self.texture = arcade.load_texture(self.player_sprite,
                                               x=self.facing*16,
                                               y=self.frame*16,
                                               width=16,
                                               height=16)

        self.center_x += self.change_x

        self.center_y += self.change_y



        # Check for out-of-bounds

        if self.left < 0:

            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:

            self.right = SCREEN_WIDTH - 1



        if self.bottom < 0:

            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:

            self.top = SCREEN_HEIGHT - 1



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None
        self.spirit_list = None
        self.tree_list = None
        self.spirit_count = 5
        self.tree_count = 5

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.spirit_list = arcade.SpriteList()
        self.tree_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(self.spirit_count):
            spirit = Spirit()
            spirit.center_x = random.randrange(SCREEN_WIDTH)
            spirit.center_y = random.randrange(SCREEN_HEIGHT)
            self.spirit_list.append(spirit)

        for i in range(self.tree_count):
            tree = Tree()
            tree.center_x = random.randrange(SCREEN_WIDTH)
            tree.center_y = random.randrange(SCREEN_HEIGHT)
            self.tree_list.append(tree)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.spirit_list.draw()
        self.tree_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        for spirit in self.spirit_list:
            spirit.follow_sprite(self.player_sprite)
        
        # Move the player

        self.player_list.update()

        hit_list = arcade.check_for_collision_with_list(self.player_list[0], self.spirit_list)
        print(hit_list)



    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """



        # If the player presses a key, update the speed

        if key == arcade.key.UP:

            self.player_sprite.change_y = MOVEMENT_SPEED

        elif key == arcade.key.DOWN:

            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT:

            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:

            self.player_sprite.change_x = MOVEMENT_SPEED



    def on_key_release(self, key, modifiers):

        """Called when the user releases a key. """



        # If a player releases a key, zero out the speed.

        # This doesn't work well if multiple keys are pressed.

        # Use 'better move by keyboard' example if you need to

        # handle this.

        if key == arcade.key.UP or key == arcade.key.DOWN:

            self.player_sprite.change_y = 0

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:

            self.player_sprite.change_x = 0



def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
