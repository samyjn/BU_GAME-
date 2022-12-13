import pygame
import os
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))     # Making screen/window

# Set Title and Game Icon
pygame.display.set_caption("Single Player")
pygame.display.set_icon(pygame.image.load(os.path.join('assets_singleplayer','ufo.png')))

# background music
mixer.music.load(os.path.join('assets_singleplayer','background.wav'))
mixer.music.play(-1)    # -1 to play is continuously


game_over_font = pygame.font.Font('freesansbold.ttf', 70)
def game_over_text():
    over_text = game_over_font.render("WASTED", True, (255,255,255))
    screen.blit(over_text, (250,250))

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)


def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(0,0,255))
    screen.blit(score,(x,y))


pX = 370
pY = 460
pX_change = 0
pY_change = 0
def player(x,y):
    screen.blit(pygame.image.load(os.path.join('assets_singleplayer','player_singleplayer.png')),(x,y))


eX  = []
eY = []
eX_change = []
eY_change = []
mIMG = []
num_enemy = 6
for i in range(num_enemy):
    eX.append(random.randint(0,736))
    eY.append(random.randint(20,70))
    eX_change.append(6)
    eY_change.append(45)
    mIMG.append(pygame.image.load(os.path.join('assets_singleplayer','enemy_singleplayer.png')))
def enemy(x,y,i):
    global enemy_state
    screen.blit(mIMG[i],(x,y))


bX = 0
bY = 460
bX_change = 0
bY_change = 40
bullet_state = "ready"
bullet_img = pygame.image.load(os.path.join('assets_singleplayer','bullet_singleplayer.png'))
bullet_img = pygame.transform.rotate(bullet_img, 90)
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img,(x+16,y+10))

def iscollison(eX,eY,bX,bY):
    dis = math.sqrt((math.pow(eX-bX, 2)) + (math.pow(eY-bY, 2)))
    if dis < 20:
        return True
    else:
        return False

# Game Loop
playing = True
while playing:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pX_change = -9
            if event.key == pygame.K_RIGHT:
                pX_change = 9
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound(os.path.join('assets_singleplayer','laser.wav'))
                    bullet_sound.play()
                    bX = pX
                    fire_bullet(bX,bY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pX_change = 0
    screen.blit(pygame.image.load(os.path.join('assets_singleplayer','bg_singleplayer.png')),(0,0))
    pX += pX_change
    if pX >= 736:
        pX = 736
    if pX <= 0:
        pX = 0
    player(pX,pY)
    for i in range(num_enemy):
        eX[i] += eX_change[i]
        if eX[i] >= 736:
            eX_change[i] = -6
            eY[i] += eY_change[i]
        elif eX[i] <= 0:
            eX_change[i] = 6
            eY[i] += eY_change[i]
        collison = iscollison(eX[i], eY[i], bX, bY)
        if collison:
            collison_sound = mixer.Sound(os.path.join('assets_singleplayer','explosion.wav'))
            collison_sound.play()
            bY = 460
            bullet_state = "ready"
            score_value += 1
            eX[i] = random.randint(0,736)
            eY[i] = random.randint(20,150)
        enemy(eX[i],eY[i],i)
        if eY[i] >= 455:
            for j in range(num_enemy):
                eY[j] = 2000
            game_over_text() 
            break
        
    if bullet_state == 'fire':
        fire_bullet(bX,bY)
        bY -= bY_change
        if bY < 0:
            bY = 460
            bullet_state = 'ready'
    show_score(10,10)
    pygame.display.update()     # Updates Display Elements