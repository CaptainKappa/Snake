import pygame
import random
import sys

def drawSnake(snakeList, block_size):
    for part in snakeList:
        pygame.draw.rect(gameDisplay, snake_color_filled, [part[0], part[1], block_size, block_size])
        pygame.draw.rect(gameDisplay, snake_color_border, [part[0], part[1], block_size, block_size], 1)

# variables
width = 300
height = 300
block_size = 10

# Snake
snakeHeadX, snakeHeadY = width/2, height/2 
snake_color_filled = (162, 224, 81)
snake_color_border = (0, 0, 0)
snakeList = []
snakeLength = 1

# directions
xForce, yForce = 0, 0
up = False
down = False
right = False
left = False

# apple
apple_color = (184, 44, 44)
appleX,appleY = None, None
ate = True

# score
score = 0

# initializing
pygame.init()
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # rules for how the snake moves
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == "w" and not down:
                xForce, yForce = 0, -1
                up = True
                down, right, left = False, False, False
            if key == "s" and not up:
                xForce, yForce = 0, 1
                down = True
                up, right, left = False, False, False
            if key == "d" and not left:
                xForce, yForce = 1, 0
                right = True
                down, up, left = False, False, False
            if key == "a" and not right:
                xForce, yForce = -1, 0
                left = True
                down, right, up = False, False, False

    # "resets" whole screen
    gameDisplay.fill((0,0,0))
    
    # spawn Apple if there is none
    if ate is True:
        appleX, appleY = random.randint(0,(width/block_size) - 1) * block_size, random.randint(0,(height/block_size) - 1) * block_size
        ate = False

        print(appleX,appleY)

    rect_Apple = pygame.Rect(appleX, appleY, block_size, block_size)
    pygame.draw.rect(gameDisplay, apple_color, rect_Apple, 0)

    # check if snake collides with apple
    if appleX == snakeHeadX and appleY == snakeHeadY:
        score += 1
        snakeLength += 1
        ate = True

    # movement for the snake
    snakeHeadX, snakeHeadY = snakeHeadX + xForce * block_size, snakeHeadY + yForce * block_size

    # updating the whole snake
    snakeHead = []
    snakeHead.append(snakeHeadX)
    snakeHead.append(snakeHeadY)
    snakeList.append(snakeHead)

    if len(snakeList) > snakeLength:
        del snakeList[0]

    drawSnake(snakeList, block_size)

    # check if snake collides with border or itself
    if snakeHeadX >= 300 or snakeHeadX <= -1 or snakeHeadY >= 300 or snakeHeadY <= -1:
        crashed = True 
    
    for i in range(len(snakeList) - 1):
        if snakeHeadX == snakeList[i][0] and snakeHeadY == snakeList[i][1]:
            crashed = True

    pygame.display.update()
    clock.tick(10)
    pass

pygame.quit()

