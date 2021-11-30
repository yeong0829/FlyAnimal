import os
import sys
import pygame
import random
from pygame import *
import tkinter as tk

pygame.init() #기본적인 초기화

scr_size = (width, height) = (700, 300)  #창 사이즈
FPS = 60    #초당 표시되는 프레임 수 정의
gravity = 0.6   #중력 가속도

black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)  #점수

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Fly Animal")

#소리
jump_sound = pygame.mixer.Sound('sprites/jump_sound.mp3')
die_sound = pygame.mixer.Sound('sprites/die_sound.mp3')
ground_sound = pygame.mixer.Sound('sprites/ground_sound.mp3')
ground_sound.play()



#첫 화면
def load_image(name, sx=-1, sy=-1, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sx != -1 or sy != -1:
        image = pygame.transform.scale(image, (sx, sy))

    return (image, image.get_rect())



def load_sprite_sheet(sheetname, nx, ny, scalex = -1, scaley = -1, colorkey = None):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j*sizex, i*sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect



def gameOver_msg(retbutton_img, gameover_img):
    retbutton_rect = retbutton_img.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_img, retbutton_rect)
    screen.blit(gameover_img, gameover_rect)



def best_record(number):
    if number > -1:
        n = []
        i = 0
        while(number / 10 != 0):
            n.append(number % 10)
            number = int(number/10)

        n.append(number % 10)
        for i in range(len(n), 5):
            n.append(0)
        n.reverse()
        return n


#동물
class Animal():
    def __init__(self, sizex=-1, sizey=-1):
        self.img,self.rect = load_sprite_sheet('fox2.png', 5, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.img[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.img[self.index]
            self.rect.width = self.stand_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1

        self.counter = (self.counter + 1)


#장애물
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed=5, sx=-1, sy=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images,self.rect = load_sprite_sheet('obstacle.png', 3, 1, sx, sy, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


#바닥
class Ground():
    def __init__(self, speed=-5):
        self.image,self.rect = load_image('ground.png', -1, -1, -1)
        self.image1,self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right



#구름
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()



#점수
class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimg,self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11*6/5), -1)
        self.image = pygame.Surface((55, int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self,score):
        score_digits = best_record(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimg[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0




#처음 시작 화면
def introscreen():
    temp_animal = Animal(80,85)     #처음 시작화면 동물 사이즈

    temp_animal.isBlinking = True
    gameStart = False

    #로고
    logo, logo_rect = load_image('logo.png', 400, 250, -1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6

    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_animal.isJumping = True
                        temp_animal.isBlinking = False
                        temp_animal.movement[1] = -1*temp_animal.jumpSpeed

        temp_animal.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)

            if temp_animal.isBlinking:      #고로삽입
                screen.blit(logo, logo_rect)
            temp_animal.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_animal.isJumping == False and temp_animal.isBlinking == False:
            gameStart = True




def gameplay():
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    player = Animal(80, 85)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Obstacle.containers = cacti
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image('replay_button.png', 35, 31, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11*6/5), -1)
    HI_image = pygame.Surface((22, int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if player.rect.bottom == int(0.98*height):
                                player.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                player.movement[1] = -1*player.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (player.isJumping and player.isDead):
                                player.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player.isDucking = False
            for c in cacti:
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(player, c):
                    player.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Obstacle(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Obstacle(gamespeed, 40, 40))

            if len(clouds) < 5 and random.randrange(0,300) == 10:
                Cloud(width,random.randrange(height/5, height/2))

            player.update()
            cacti.update()
            clouds.update()
            new_ground.update()
            scb.update(player.score)
            highsc.update(high_score)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                player.draw()

                pygame.display.update()
            clock.tick(FPS)

            if player.isDead:
                gameOver = True
                if player.score > high_score:
                    high_score = player.score

            if counter%700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()
            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                gameOver_msg(retbutton_image, gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()