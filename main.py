import pygame
from pygame import mixer
import random
import math

# Initialise the pygame instance
pygame.init()

# Initialising the screen
screen = pygame.display.set_mode((800, 600))

# Backgrounds
background = pygame.image.load('background.png')
game_over = pygame.image.load('game_over.png')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Intruders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# bullet
# Ready - bullet is not visible
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

# explosion
explosionImg = pygame.image.load('explosion.png')
explosionX = 0
explosionY = 0
explosion_state = "ready"

# score

score_value = 0
font = pygame.font.Font('Pixeled.ttf', 24)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('Pixeled.ttf', 42)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 4))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Checking for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB - Red, Green, Blue
    playerX += playerX_change

    # Setting the player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            screen.blit(game_over, (0, 0))
            playerX_change = 0
            explosionX = playerX
            explosionY = playerY
            explosion(explosionX, explosionY)
            break

        enemyX[i] += enemyX_change[i]

        # Setting the enemy boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            explosionX = enemyX[i]
            explosionY = enemyY[i]
            enemyX_change[i] = 0
            explosion(explosionX, explosionY)

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            enemyX_change[i] = 5

        enemy(enemyX[i], enemyY[i], i)

    # resetting the bullet
    if bulletY <= 0:
        bulletY = 440
        bullet_state = "ready"

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Initialising the player
    player(playerX, playerY)
    show_score(textX, textY)

    # Updating the display
    pygame.display.update()
