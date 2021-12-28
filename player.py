import pygame
from support_func import open_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.apply_character_assets()
        self.frame_index = 0
        self.animation_update_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.is_jump = 1

        # player status
        self.status = 'idle'
        self.player_facing_right = True
        
        # collision types
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
       
    # creates player model animation
    def apply_character_assets(self):
        character_path = 'sprites/character'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            # open_folder() imported from support_func
            self.animations[animation] = open_folder(full_path)
    
    # animating the character
    def animate_character(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_update_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.player_facing_right:
            self.image = image
        else:
            # reversing image transform.flip(file, reverse - x.condition / y.condition (True / False))
            reversed_image = pygame.transform.flip(image, True, False)
            self.image = reversed_image

        # setting the right rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
    
    # reacting to the keyboard input
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.player_facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.player_facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
    
    # changing self.status depending on different player movements
    def get_character_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    
    # support func, used in level.py/class Level/def vertical_movement_collision(self)
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_character_status()
        self.animate_character()




