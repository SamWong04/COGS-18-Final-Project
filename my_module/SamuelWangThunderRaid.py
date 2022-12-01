import pygame
import random
from pygame.locals import *
from classfile import *
from sys import exit

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Samuel Wangs Thunder Raid')

# Load the background musics
bullet_sound = pygame.mixer.Sound('res/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('res/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('res/sound/game_over.wav')
bullet_sound.set_volume(0.5)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('res/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Load the background
background = pygame.image.load('res/image/background.jpg').convert()
game_over = pygame.image.load('res/image/gameover.png')

filename = 'res/image/shoot.png'
plane_img = pygame.image.load(filename)

# Set the player's image parameters
player_rect = []
# The area of player on the image file
# (left, Top, Width, Height)pixel
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
# The area of hitted player on the image file
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# The initial position of player
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# Set the plaer's bullet's image parameters
player_bullet_rect = pygame.Rect(1004, 987, 9, 21)
player_bullet_img = plane_img.subsurface(player_bullet_rect)

# Set the protector'bullet's image parameters
protector_bullet_rect = pygame.Rect(67, 77, 9, 21)
protector_bullet_img = plane_img.subsurface(protector_bullet_rect)

# Set the enemies' image parameters
enemy1_rect = pygame.Rect(534, 612, 57, 43)  # (left, Top, Width, Height)pixel
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()
# Save the hitted enemy to render the destoried animation
enemies_down = pygame.sprite.Group()


# Set the protector' parameters
protector_rect = []
# THe are of protector on the image file
# (left, Top, Width, Height) pixel
protector_rect.append(pygame.Rect(336, 750, 168, 254))
protector_rect.append(pygame.Rect(505, 750, 168, 254))
# The area of hitted protector on the image file
protector_rect.append(pygame.Rect(0, 492, 168, 254))
protector_rect.append(pygame.Rect(0, 233, 168, 254))
protector_rect.append(pygame.Rect(168, 489, 168, 254))
protector_rect.append(pygame.Rect(679, 750, 168, 254))
# The initial position of player
protector_pos = [100, 200]
protector = Player(plane_img, protector_rect, protector_pos)


player_shoot_frequency = 0
protector_shoot_frequency = 0
enemy_frequency = 0
protector_frequency = 0

player_down_index = 16
protector_down_index = 50

score = 0

clock = pygame.time.Clock()

running = True

while running:
    # Set the maximum refresh rate at 60fps
    clock.tick(45)

    # Contorl the frequency of shooting the bullet
    if not player.is_hit:
        if player_shoot_frequency % 15 == 0:
            bullet_sound.play()
            player.shoot(player_bullet_img)
        player_shoot_frequency += 1
        if player_shoot_frequency >= 15:
            player_shoot_frequency = 0

    # Contorl the frequency of shooting the bullet
    if not protector.is_hit:
        if protector_shoot_frequency % 15 == 0:
            bullet_sound.play()
            protector.shoot(protector_bullet_img)
        protector_shoot_frequency += 2
        if protector_shoot_frequency >= 15:
            protector_shoot_frequency = 0

    # Generate the enemy
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # Move the bullet and delete them when out of the visible window
    for bullet in player.bullets:
        bullet.move(True)
        if bullet.rect.bottom < 0 or pygame.sprite.groupcollide(protector.bullets, player.bullets, 1, 1):
            player.bullets.remove(bullet)

    # Move the bullet and delete them when out of the visible window
    for bullet in protector.bullets:
        bullet.move(False)
        if bullet.rect.bottom > 500:
            protector.bullets.remove(bullet)

    # Move the enemy and delete them when out of the visible window
    for enemy in enemies1:
        enemy.move()
        # Judge whether the player is hitted
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # Add the hitted enemies in the group to render the hitted animation
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # Render the background
    screen.fill(0)
    screen.blit(background, (0, 0))

    # Render the player
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # Change the index of the image to add animation, the smoke after the engine
        player.img_index = player_shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # Render the protector
    if not protector.is_hit:
        screen.blit(protector.image[protector.img_index], protector.rect)
        # Change the index of the image to add animation, the smoke after the engine
        protector.img_index = protector_shoot_frequency // 8
    else:
        protector.img_index = protector_down_index // 8
        screen.blit(protector.image[protector.img_index], protector.rect)
        protector_down_index += 1
        if protector_down_index > 47:
            running = False

    # Render the hitted animation
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(
            enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)

    # Render the bullets and the enemies
    player.bullets.draw(screen)
    protector.bullets.draw(screen)
    enemies1.draw(screen)

    # Render the score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # Refresh the display
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Continuously listening the keyboard event to check the player's input
    key_pressed = pygame.key.get_pressed()
    # If the player is hitted then cannot input the movement
    if not player.is_hit:
        if key_pressed[K_w]:
            player.moveup()
        if key_pressed[K_s]:
            player.movedown()
        if key_pressed[K_a]:
            player.moveleft()
        if key_pressed[K_d]:
            player.moveright()

    if not protector.is_hit:
        if key_pressed[K_UP]:
            protector.moveup()
        if key_pressed[K_DOWN]:
            protector.movedown()
        if key_pressed[K_LEFT]:
            protector.moveleft()
        if key_pressed[K_RIGHT]:
            protector.moveright()

# Read the font file for the display
font = pygame.font.Font(None, 48)
text = font.render('Score: ' + str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

# Quit the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
