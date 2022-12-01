import pygame
import random

# Screen resolution
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768


class Bullet(pygame.sprite.Sprite):
    '''
    The bullets of both Players(the attacker and the defender)

    Parameters
    ----------
    bullet_img:
        the image of the bullet
    init_pos:
        the initial position of the bullet
    '''

    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self, up):
        '''
        The movement of the bullet, it whether move upward or downward

        Parameters
        ----------
        up: boolean
            if it's True, the bullet will move upward
            if it's False, the bullet will move downward
        '''
        if up:
            self.rect.top -= self.speed
        else:
            self.rect.top += self.speed


class Player(pygame.sprite.Sprite):
    '''
    The Players class

    The attacker and the defender that controlled by the player are the instances of the Player class
    It's a sprite type of object, in the pygame doc:"Simple base class for visible game objects."

    Parameters
    ----------
    plane_img:
        the image that contains all the needed pictures including different status of planes.
    player_rect:
        pygame object for storing rectangular coordinates
        Rect(left, top, width, height)
    init_pos:
        The initial position of the object
    '''

    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)

        # The list that stored the player's image
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(
                player_rect[i]).convert_alpha())

        # Initialize the square of the plaer
        self.rect = player_rect[0]

        # Initialize the upleft position of player's square
        self.rect.topleft = init_pos

        # Initializ the speed of the player
        self.speed = 8

        # The group of shoot bullets
        self.bullets = pygame.sprite.Group()

        # The index of the current player's image
        self.img_index = 0

        # Player's status
        self.is_hit = False

    def shoot(self, bullet_img):
        '''
        Shoot the bullet

        Parameters
        ----------
        bullet_img: 
            the image of the bullet
        '''
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveup(self):
        '''
        Move the object upward by reducing the top coordinate by its setted speed.
        Also set the limit, the top coordinate cannot lower than 0, cannot move out of the screen
        '''
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def movedown(self):
        '''
        Move the object downward by reducing the top coordinate by its setted speed.
        Also set the limit, the top coordinate cannot lower than the lower boundary of the screen
        '''
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveleft(self):
        '''
        Move the object leftward by reducing the top coordinate by its setted speed.
        Also set the limit, the left coordinate cannot lower than 0, cannot move out of the screen
        '''
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveright(self):
        '''
        Move the object rightward by reducing the top coordinate by its setted speed.
        Also set the limit, ensure the object will not move outside the screen
        '''
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    '''
    The Enemy class (The random generate little plane, defenders)

    It's a sprite type of object. A simple base class for visible game objects."

    Parameters
    ----------
    enemy_img:
        the image that contains all the needed pictures including different status of planes.
    enemy_down_imgs:
        A series of image when the little plane is hitted by the attacker, animation of explosion
    init_pos:
        The initial position of the object
    '''

    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        '''
        move the object downward while move left and right with random units to escape from the attackers
        '''
        self.rect.top += self.speed
        self.rect.left -= self.speed * random.randint(0, 2)  # Move Left
        self.rect.left += self.speed * random.randint(0, 2)  # Move Right
