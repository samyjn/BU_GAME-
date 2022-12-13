import pygame
import os

pygame.init()

WIN = pygame.display.set_mode((900,500))
pygame.display.set_caption('multiplayer')

BORDER = pygame.Rect(445, 0, 10, 500)

VEL = 5     #velocity of spaceships

MAX_BULLETS = 3
VEL_BULLETS = 8


RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 56

RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BLUE_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def draw_window(red,blue,red_bullets,blue_bullets):
    WIN.fill((255,255,255))
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    WIN.blit(RED_SPACESHIP, (red.x,red.y))
    WIN.blit(BLUE_SPACESHIP,(blue.x,blue.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, ((255,0,0)), bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(WIN, ((0,0,255)), bullet)

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < (BORDER.x-SPACESHIP_HEIGHT):
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + SPACESHIP_WIDTH + VEL < 500:
        red.y += VEL

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > BORDER.x + 10:
        blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x +SPACESHIP_HEIGHT + VEL < 900:
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0:
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + SPACESHIP_WIDTH + VEL < 500:
        blue.y += VEL

def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += VEL_BULLETS
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > 900:
            red_bullets.remove(bullet)
            
    for bullet in blue_bullets:
        bullet.x -= VEL_BULLETS
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


def main():
    red = pygame.Rect(20, 215, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Rectange of red spaceship
    blue = pygame.Rect(830, 215, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Rectange of blue spaceship

    red_bullets = []
    blue_bullets = []

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x + SPACESHIP_HEIGHT, red.y + (SPACESHIP_WIDTH)//2, 8, 5)
                red_bullets.append(bullet)

            if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(blue.x, blue.y + (SPACESHIP_WIDTH)//2, 8, 5)
                blue_bullets.append(bullet)
        
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        blue_handle_movement(keys_pressed, blue)
        handle_bullets(red_bullets, blue_bullets, red, blue)
        
        draw_window(red, blue, red_bullets, blue_bullets)
    
main()