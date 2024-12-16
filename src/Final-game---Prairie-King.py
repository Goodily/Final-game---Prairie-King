# Our group wanted to make a Snake game, but I really liked Stardew Valley, so I made an additional game myself.
# 钟心悦 1210020883 大四 商学院金融

import sys, pygame, pygame.mixer
import random
from pygame.locals import *

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# user
class User(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # construct the parent component
        self.image = pygame.image.load("../assets/images/facing up.png").convert_alpha()
        self.facing = 0  # 0 is up, 1 is down, 2 is left, and 3 is right
        self.rect = self.image.get_rect()
        self.rect.topleft = (320, 240)
        self.dir_x = 1
        self.dir_y = 1
        self.delta = (0, 0)

    def update(self):
        # Move the sprite based on speed
        self.rect.move_ip(self.delta[0], self.delta[1])
        self.delta = (0, 0)

    def movement(self, delta):
        self.delta = delta
        if self.rect.topleft[0] - self.delta[0] < 23 and self.facing == 2:
            self.delta = (0, self.delta[1])
        elif self.rect.topleft[0] + self.delta[0] > screen.get_width() - 23 and self.facing == 3:
            self.delta = (0, self.delta[1])
        if self.rect.topleft[1] - self.delta[1] < 23 and self.facing == 0:
            self.delta = (self.delta[0], 0)
        elif self.rect.topleft[1] + self.delta[1] > screen.get_height() - 23 and self.facing == 1:
            self.delta = (self.delta[0], 0)

    def change_image_up(self):
        self.image = pygame.image.load("../assets/images/facing up.png").convert_alpha()
        self.facing = 0

    def change_image_down(self):
        self.image = pygame.image.load("../assets/images/facing down.png").convert_alpha()
        self.facing = 1

    def change_image_left(self):
        self.image = pygame.image.load("../assets/images/facing left.png").convert_alpha()
        self.facing = 2

    def change_image_right(self):
        self.image = pygame.image.load("../assets/images/facing right.png").convert_alpha()
        self.facing = 3


# entity
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # construct the parent component
        self.image = pygame.image.load("../assets/images/Entity.png").convert_alpha()
        self.rect = self.image.get_rect()

        spawn_choice = random.randint(0, 3)
        if spawn_choice == 0:
            init_pos = (23, 240)
            direction = (1, 0)
        elif spawn_choice == 1:
            init_pos = (617, 240)
            direction = (-1, 0)
        elif spawn_choice == 2:
            init_pos = (320, 23)
            direction = (0, 1)
        elif spawn_choice == 3:
            init_pos = (320, 457)
            direction = (0, -1)

        self.rect.topleft = init_pos
        self.dir_x = direction[0]
        self.dir_y = direction[1]
        self.speed = 1

    def update(self, player_pos):  # dir_x = 1 is right, dir_x = -1 is left,
        if player_pos[0] > self.rect.topleft[0]:
            self.dir_x = 1
        elif player_pos[0] < self.rect.topleft[0]:
            self.dir_x = -1
        else:
            self.dir_x = 0

        if player_pos[1] > self.rect.topleft[1]:
            self.dir_y = 1
        elif player_pos[1] < self.rect.topleft[1]:
            self.dir_y = -1
        else:
            self.dir_y = 0

        if self.dir_x != 0 and self.dir_y != 0:
            if random.randint(0, 1) == 0:
                self.dir_x = 0
            else:
                self.dir_y = 0
        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)


# bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../assets/images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.dir_x = direction[0]
        self.dir_y = direction[1]
        self.speed = 1

    def update(self):
        if self.rect.left < 20 or self.rect.right >= screen.get_width() - 20:
            self.kill()
        if self.rect.top < 20 or self.rect.bottom >= screen.get_height() - 20:
            self.kill()
        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)


# background
start_bg = pygame.image.load("../assets/images/start screen.png")
game_bg = pygame.image.load("../assets/images/Background.png")
gameover1_bg = pygame.image.load("../assets/images/game over 1.png")
gameover2_bg = pygame.image.load("../assets/images/game over 2.png")
tutorial_bg = pygame.image.load("../assets/images/Tutorial.png")
win_bg = pygame.image.load("../assets/images/Win_Screen.png")


screen = pygame.display.set_mode((640, 480))
bullet_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
character = User()
character_group = pygame.sprite.Group(character)
bounce = pygame.mixer.Sound("../assets/sounds/gun fire.wav")
bounce.set_volume(0.3)

pygame.mixer.music.load("../assets/sounds/Outlaw.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
my_font = pygame.font.Font("../assets/fonts/Pacifico.ttf", 20)

bg_id = 0
num_entity = 0
game_turn = 0
kill_count = 0
keep_going = True
win_kill_count = 30

# move
while keep_going:

    clock.tick(80)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == QUIT:
            keep_going = False
            break
        if event.type == KEYDOWN:
            if bg_id == 4:
                bg_id = 1
            elif bg_id == 5:
                bg_id = 0

            if event.key == K_SPACE:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("../assets/sounds/Final Boss.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                if bg_id == 0:
                    bg_id = 4

            elif event.key == K_RETURN:
                if bg_id == 3:
                    keep_going = False
                    break
                elif bg_id == 2:
                    bullet_group.empty()
                    entity_group.empty()

                    character = User()
                    character_group = pygame.sprite.Group(character)
                    bg_id = 1

            elif event.key == K_UP:
                if bg_id == 1:
                    if character.facing == 0:
                        bullet = Bullet(character.rect.topleft, (0, -1))
                        bullet_group.add(bullet)
                        bounce.play()
                elif bg_id == 3:
                    bg_id = 2

            elif event.key == K_DOWN:
                if bg_id == 1:
                    if character.facing == 1:
                        bullet = Bullet(character.rect.topleft, (0, 1))
                        bullet_group.add(bullet)
                        bounce.play()
                elif bg_id == 2:
                    bg_id = 3

            elif event.key == K_LEFT:
                if bg_id == 1:
                    if character.facing == 2:
                        bullet = Bullet(character.rect.topleft, (-1, 0))
                        bullet_group.add(bullet)
                        bounce.play()

            elif event.key == K_RIGHT:
                if bg_id == 1:
                    if character.facing == 3:
                        bullet = Bullet(character.rect.topleft, (1, 0))
                        bullet_group.add(bullet)
                        bounce.play()


        elif keys[pygame.K_w]:
            if bg_id == 1:
                character.movement((0, -4))
                character.change_image_up()
        elif keys[pygame.K_s]:
            if bg_id == 1:
                character.movement((0, 4))
                character.change_image_down()
        elif keys[pygame.K_a]:
            if bg_id == 1:
                character.movement((-4, 0))
                character.change_image_left()
        elif keys[pygame.K_d]:
            if bg_id == 1:
                character.movement((4, 0))
                character.change_image_right()


    if bg_id == 0:
        screen.fill((0, 0, 0))
        screen.blit(start_bg, (0, 0))
        pygame.display.update()
        game_turn = 0
    elif bg_id == 1:

        if game_turn % random.randint(50, 100) == 1:
            num_entity = 1
            entity_list = []

            for entity_id in range(num_entity):
                entity = Entity()
                entity_list.append(entity)
            entity_group.add(entity_list)

        entity_before_total = len(entity_group.sprites())
        pygame.sprite.groupcollide(bullet_group, entity_group, True, True)
        entity_after_total = len(entity_group.sprites())
        kill_count += (entity_before_total - entity_after_total)
        label = my_font.render(f"{kill_count}/{win_kill_count}", False, (0, 0, 0))
        pygame.sprite.groupcollide(character_group, entity_group, True, False)

        if len(character_group.sprites()) == 0:
            bg_id = 2

        character_group.clear(screen, game_bg)
        character_group.update()
        bullet_group.clear(screen, game_bg)
        bullet_group.update()
        entity_group.clear(screen, game_bg)
        entity_group.update(character.rect.topleft)

        screen.blit(game_bg, (0, 0))
        bullet_group.draw(screen)
        character_group.draw(screen)
        entity_group.draw(screen)
        screen.blit(label, (20, 20))
        pygame.display.flip()
        game_turn += 1


        if kill_count >= win_kill_count:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../assets/sounds/Ending.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            bg_id = 5
    elif bg_id == 2:
        screen.blit(gameover1_bg, (0, 0))
        pygame.display.update()

        kill_count = 0
    elif bg_id == 3:
        screen.blit(gameover2_bg, (0, 0))
        pygame.display.update()
    elif bg_id == 4:
        screen.blit(tutorial_bg, (0, 0))
        pygame.display.update()
    elif bg_id == 5:

        screen.blit(win_bg, (0, 0))
        pygame.display.update()
        kill_count = 0
        bullet_group.empty()
        entity_group.empty()
        character_group.empty()
        character = User()
        character_group = pygame.sprite.Group(character)