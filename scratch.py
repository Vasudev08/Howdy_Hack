import pygame
import math
import random

def main():
    pygame.init()

    #Window
    logo  = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("HowdyHack Program")

    #Player
    playerImg = pygame.image.load("pixil-frame-0.png")
    playerX = 400
    playerY = 400
    playerXChange = 0.0
    playerYChange = 0.0
    playerSpeed = 0.2

    def player(x, y):
        screen.blit(playerImg, (x, y))

    #Enemy
    enemyImg = pygame.image.load("pixil-frame-0.png")
    enemyX = random.randint(100, 600)
    enemyY = 100
    enemyXChange = 0.1
    enemyYChange = 30.0

    def enemy(x, y):
        screen.blit(enemyImg, (x, y))
    

    #Screen
    screen = pygame.display.set_mode((800, 600))

    #Session
    running = True

    while running:

        #RGB for background
        screen.fill((100, 0, 0))

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    playerXChange = -playerSpeed
                if event.key == pygame.K_d:
                    playerXChange = playerSpeed
                if event.key == pygame.K_w:
                    playerYChange = -playerSpeed
                if event.key == pygame.K_s:
                    playerYChange = playerSpeed
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    playerXChange = 0.0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    playerYChange = 0.0
                

        playerX += playerXChange
        if playerX <= 0:
            playerX = 0
        if playerX >= 700:
            playerX = 700

        playerY += playerYChange
        if playerY <= 0:
            playerY = 0
        if playerY >= 500:
            playerY = 500

        enemyX += enemyXChange
        if enemyX <= 0:
            enemyX = 0
            enemyXChange *= -1
            enemyY += enemyYChange
        if enemyX >= 700:
            enemyX = 700
            enemyXChange *= -1
            enemyY += enemyYChange

        enemy(enemyX, enemyY)
        player(playerX, playerY)
        pygame.display.update()

if __name__ == "__main__":
    main()