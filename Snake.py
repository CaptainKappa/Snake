import pygame
import random
import sys

WIN_WIDTH = 300
WIN_HEIGHT = 300
BLOCK_SIZE = 10

class Snake:
    COLOR_FILLED = (162, 224, 81)
    COLOR_BORDER = (0, 0, 0)


    def __init__(self):
        self.x = 150
        self.y = 150
        self.length = 1
        self.body = []
        self.xForce = 0
        self.yForce = 0
        self.direction = None


    def move(self):
        self.x += self.xForce * BLOCK_SIZE
        self.y += self.yForce * BLOCK_SIZE


    def changeForce(self,key):
        if key == "w" and self.direction != "down":
            self.xForce, self.yForce = 0, -1
            self.direction = "up"
        elif key == "s" and self.direction != "up":
            self.xForce, self.yForce = 0, 1
            self.direction = "down"
        elif key == "a" and self.direction != "right":
            self.xForce, self.yForce = -1, 0
            self.direction = "left"
        elif key == "d" and self.direction != "left": 
            self.xForce, self.yForce = 1, 0
            self.direction = "right"


    def draw(self, win):
        snakeHead = []
        snakeHead.append(self.x)
        snakeHead.append(self.y)
        self.body.append(snakeHead)

        if len(self.body) > self.length:
            del self.body[0]

        for element in self.body:
            pygame.draw.rect(win, self.COLOR_FILLED, [element[0], element[1], BLOCK_SIZE, BLOCK_SIZE])
            pygame.draw.rect(win, self.COLOR_BORDER, [element[0], element[1], BLOCK_SIZE, BLOCK_SIZE], 1)


    def colApple(self, apple):
        if self.x == apple.x and self.y == apple.y:
            apple.ate = True
            self.length += 1
            return True
        else:
            return False


    def colWall(self):
        if self.x >= 300 or self.x <= -1 or self.y >= 300 or self.y <= -1:
            return True


    def colBody(self):
        for i in range(len(self.body) - 1):
            if self.x == self.body[i][0] and self.y == self.body[i][1]:
                return True


class Apple:
    COLOR = (184, 44, 44)
    

    def __init__(self):
        self.x = random.randint(0,(WIN_WIDTH/BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0,(WIN_HEIGHT/BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.ate = False

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])


# GAME HANDLING 

def draw_window(win, snake, apple):
    win.fill((0,0,0))
    snake.draw(win)
    apple.draw(win)
    pygame.display.update()


def main():
    snake = Snake()
    apple = Apple()
    win = pygame.display.set_mode((WIN_HEIGHT,WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    snake.changeForce(key)

        snake.move()
        
        if snake.colApple(apple):
            print("COLLISION APPLE")
            apple = Apple()
            score += 1
        elif snake.colWall():
            print("TODO GAME OVER")
        elif snake.colBody():
            print("TODO GAME OVER")
            
        draw_window(win, snake, apple)

    pygame.quit()
    quit()

main()

