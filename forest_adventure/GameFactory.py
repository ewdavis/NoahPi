import pygame

SOUTH = 0
NORTH = 1
WEST = 2
EAST = 3

class GFAI():

    def __init__(self):
        self.state = 0
        self.x_change = 0
        self.y_change = 0

class GFFollowAI(GFAI):

    def __init__(self, enemy_character, character):
        super().__init__()
        self.ai = enemy_character
        self.target = character

    def update(self, update_speed):
        self.x_change = (self.ai.pos_x - self.target.pos_x)
        self.y_change = (self.ai.pos_y - self.target.pos_y)

        if abs(self.x_change) > abs(self.y_change):
            if (self.x_change) > 0:
                self.ai.facing = WEST
            else:
                self.ai.facing = EAST
        else:
            if (self.y_change) > 0:
                self.ai.facing = NORTH
            else:
                self.ai.facing = SOUTH

        self.ai.animation_state = self.ai.animation_state + update_speed
        if (self.ai.animation_state > self.ai.max_animation_state):
            self.ai.animation_state = 0
            
        self.ai.image = self.ai.sprite_sheet.get_image(self.ai.facing,
                                                     int(self.ai.animation_state),
                                                     self.ai.sprite_width,
                                                     self.ai.sprite_height,
                                                     self.ai.sprite_scale,
                                                     self.ai.alpha_color)

        if self.ai.pos_y < self.target.pos_y:
            self.ai.pos_y += min(self.ai.speed, self.target.pos_y - self.ai.pos_y)
        elif self.ai.pos_y > self.target.pos_y:
            self.ai.pos_y -= min(self.ai.speed, self.ai.pos_y - self.target.pos_y)

        if self.ai.pos_x < self.target.pos_x:
            self.ai.pos_x += min(self.ai.speed, self.target.pos_x - self.ai.pos_x)
        elif self.ai.pos_x > self.target.pos_x:
            self.ai.pos_x -= min(self.ai.speed, self.ai.pos_x - self.target.pos_x)

        if self.ai.pos_x <= 0:
            self.ai.pos_x = 0
        if self.ai.pos_x >= (self.ai.screen_width_bound - self.ai.sprite_width*2):
            self.ai.pos_x = (self.ai.screen_width_bound - self.ai.sprite_width*2)
        if self.ai.pos_y <= 0:
            self.ai.pos_y = 0
        if self.ai.pos_y >= (self.ai.screen_height_bound - self.ai.sprite_height*2):
            self.ai.pos_y = (self.ai.screen_height_bound - self.ai.sprite_height*2)

        self.ai.rect = self.ai.image.get_rect()
        self.ai.rect.topleft = [self.ai.pos_x, self.ai.pos_y]

class GFScreen():

    def __init__(self, screen_width=800, screen_height=600):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_width(self):
        return(self.screen_width)

    def get_height(self):
        return(self.screen_height)

    def fill(self, color):
        self.screen.fill(color)

class GFSpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_i, frame_j, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_i * width),
                                        (frame_j * height),
                                        width,
                                        height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

class GFBasic_Monster(pygame.sprite.Sprite):

    def __init__(self, sprite_path,
                     sprite_width = 16,
                     sprite_height = 16,
                     sprite_scale = 2.0,
                     alpha_color = (0, 0, 0),
                     init_pos_x = 0,
                     init_pos_y = 0,
                     facing = SOUTH,
                     animation_state = 0,
                     max_animation_state = 3,
                     screen_width_bound = 800,
                     screen_height_bound = 600):
        super().__init__()
        self.sprite_sheet_image = pygame.image.load(sprite_path)
        self.sprite_sheet = GFSpriteSheet(self.sprite_sheet_image)
        self.sprite_width = sprite_width        
        self.sprite_height = sprite_height
        self.sprite_scale = sprite_scale
        self.alpha_color = alpha_color
        self.speed = 0.5
        
        self.facing = SOUTH
        self.animation_state = 0
        self.max_animation_state = 3
        self.image = self.sprite_sheet.get_image(self.facing,
                                                     self.animation_state,
                                                     self.sprite_width,
                                                     self.sprite_height,
                                                     self.sprite_scale,
                                                     self.alpha_color)
        self.screen_width_bound = screen_width_bound
        self.screen_height_bound = screen_height_bound
        
        self.rect = self.image.get_rect()
        self.pos_x = init_pos_x
        self.pos_y = init_pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.ai = None

    def set_screen(self, myscreen):
        self.screen_width = myscreen.get_width()
        self.screen_height = myscreen.get_height()

    def update(self, speed):

        if (self.ai is not None):
            self.ai.update(speed)
            return()
        
        self.animation_state += speed
        if (self.animation_state > self.max_animation_state):
            self.animation_state = 0
        self.image = self.sprite_sheet.get_image(self.facing,
                                                     int(self.animation_state),
                                                     self.sprite_width,
                                                     self.sprite_height,
                                                     self.sprite_scale,
                                                     self.alpha_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

        if self.pos_x <= 0:
            self.pos_x = 0
        if self.pos_x >= (self.screen_width_bound - self.sprite_width*2):
            self.pos_x = (self.screen_width_bound - self.sprite_width*2)
        if self.pos_y <= 0:
            self.pos_y = 0
        if self.pos_y >= (self.screen_height_bound - self.sprite_height*2):
            self.pos_y = (self.screen_height_bound - self.sprite_height*2)

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

class GFCharacter(pygame.sprite.Sprite):

    def __init__(self, sprite_path,
                     sprite_width = 16,
                     sprite_height = 16,
                     sprite_scale = 2.0,
                     alpha_color = (0, 0, 0),
                     init_pos_x = 0,
                     init_pos_y = 0,
                     facing = SOUTH,
                     animation_state = 0,
                     max_animation_state = 3,
                     screen_width_bound = 800,
                     screen_height_bound = 600):
        super().__init__()
        self.sprite_sheet_image = pygame.image.load(sprite_path)
        self.sprite_sheet = GFSpriteSheet(self.sprite_sheet_image)
        self.sprite_width = sprite_width        
        self.sprite_height = sprite_height
        self.sprite_scale = sprite_scale
        self.alpha_color = alpha_color

        self.facing = facing
        self.animation_state = animation_state
        self.max_animation_state = max_animation_state

        self.image = self.sprite_sheet.get_image(self.facing,
                                                 self.animation_state,
                                                 self.sprite_width,
                                                 self.sprite_height,
                                                 self.sprite_scale,
                                                 self.alpha_color)
        self.screen_width_bound = screen_width_bound
        self.screen_height_bound = screen_height_bound
        
        self.rect = self.image.get_rect()
        self.pos_x = init_pos_x
        self.pos_y = init_pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.change_x = 0
        self.change_y = 0

    def set_screen(self, myscreen):
        self.screen_width = myscreen.get_width()
        self.screen_height = myscreen.get_height()

    def update(self, update_speed):

        if (self.change_x != 0) or (self.change_y != 0):
            self.animation_state += update_speed
        if self.animation_state > self.max_animation_state:
            self.animation_state = 0

        if self.change_x > 0:
            self.facing = 3
        elif self.change_x < 0:
            self.facing = 2
        elif self.change_y > 0:
            self.facing = 0
        elif self.change_y < 0:
            self.facing = 1
            
        self.image = self.sprite_sheet.get_image(self.facing,
                                                 int(self.animation_state),
                                                 self.sprite_width,
                                                 self.sprite_height,
                                                 self.sprite_scale,
                                                 self.alpha_color)

        self.pos_x += self.change_x
        self.pos_y += self.change_y

        if self.pos_x <= 0:
            self.pos_x = 0
        if self.pos_x >= (self.screen_width_bound - self.sprite_width*2):
            self.pos_x = (self.screen_width_bound - self.sprite_width*2)
        if self.pos_y <= 0:
            self.pos_y = 0
        if self.pos_y >= (self.screen_height_bound - self.sprite_height*2):
            self.pos_y = (self.screen_height_bound - self.sprite_height*2)

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
                                                 
        
