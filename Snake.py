import pygame
import pygame.font
import random

WIN_WIDTH = 300
WIN_HEIGHT = 300
BLOCK_SIZE = 10

class Snake:
    COLOR_FILLED = (0, 0, 0)
    COLOR_BORDER = (99, 163, 96)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 1
        self.body = []
        self.xForce = 0
        self.yForce = 0
        self.direction = None

    def move(self):
        self.x += self.xForce * BLOCK_SIZE
        self.y += self.yForce * BLOCK_SIZE

    def changeForce(self, key):
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
        if self.x >= 281 or self.x <= 9 or self.y >= 281 or self.y <= 9:
            return True

    def colBody(self):
        for i in range(len(self.body) - 1):
            if self.x == self.body[i][0] and self.y == self.body[i][1]:
                return True


class Apple:
    COLOR_FILLED = (184, 44, 44)
    COLOR_BORDER = (99, 163, 96)

    def __init__(self, snakeBody):
        while True:
            self.x = random.randint(1,(WIN_WIDTH/BLOCK_SIZE) - 2) * BLOCK_SIZE
            self.y = random.randint(1,(WIN_HEIGHT/BLOCK_SIZE) - 2) * BLOCK_SIZE
        
            if not self.checkOccupied(snakeBody):
                break

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR_FILLED, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(win, self.COLOR_BORDER, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE], 1)

    def checkOccupied(self, snakeBody):
        for element in snakeBody:
            if element[0] == self.x and element[1] == self.y:
                return True
            else:
                return False

# START SCREEN

class Start:
    pygame.init()
    SNAKEFONT = pygame.font.SysFont("Power Red and Green", 60)
    SCOREFONT = pygame.font.SysFont("Power Red and Green", 20)
    PLAYFONT = pygame.font.SysFont("Power Red and Green", 30)
    EXITFONT = pygame.font.SysFont("Power Red and Green", 30)

    def __init__(self, score):
        self.snakeLabel = self.SNAKEFONT.render("SNAKE", 1, (0, 0, 0))
        self.scoreLabel = self.SCOREFONT.render("Score: " + str(score), 1, (0, 0, 0))
        self.playLabel = self.PLAYFONT.render("Play", 1, (0, 0, 0))
        self.exitLabel = self.EXITFONT.render("Exit", 1, (0, 0, 0))

        self.snake = Snake(10, 10)
        self.snake.length = 40

        self.running = True

    def drawSnake(self, win):
        if self.snake.x == 10 and self.snake.y == 10:
            self.snake.xForce, self.snake.yForce = 1, 0
        elif self.snake.x == 280 and self.snake.y == 10:
            self.snake.xForce, self.snake.yForce = 0, 1
        elif self.snake.x == 280 and self.snake.y == 280:
            self.snake.xForce, self.snake.yForce = -1, 0
        elif self.snake.x == 10 and self.snake.y == 280: 
            self.snake.xForce, self.snake.yForce = 0, -1
        self.snake.move()
        win.fill((99, 163, 96))
        self.snake.draw(win)

    def renderMenu(self, mousePos):
        if (120 <= mousePos[0] <= 170) and (140 <= mousePos[1] <= 160):
            self.PLAYFONT.set_underline(True)
            self.PLAYFONT.set_bold(True)
        else:
            self.PLAYFONT.set_underline(False)
            self.PLAYFONT.set_bold(False)

        if (120 <= mousePos[0] <= 170) and (170 <= mousePos[1] <= 190):
            self.EXITFONT.set_underline(True)
            self.EXITFONT.set_bold(True)
        else:
            self.EXITFONT.set_underline(False)
            self.EXITFONT.set_bold(False)
           
        self.playLabel = self.PLAYFONT.render("Play", 1, (0, 0, 0))
        self.exitLabel = self.EXITFONT.render("Exit", 1, (0, 0, 0))

    def draw_window_start(self, win, mousePos):
        self.drawSnake(win)
        self.renderMenu(mousePos)

        win.blit(self.snakeLabel, (80,60))
        win.blit(self.playLabel, (120, 140))
        win.blit(self.exitLabel, (120, 170))
        win.blit(self.scoreLabel, (110, 250))
        pygame.display.flip()

    def clickButton(self, mousePos):
        if (120 <= mousePos[0] <= 170) and (140 <= mousePos[1] <= 160):
            self.running = False
            main()
        if (120 <= mousePos[0] <= 170) and (170 <= mousePos[1] <= 190):
            self.running = False


# RUNNING GAME

def draw_window_play(win, snake, apple):
    win.fill((99, 163, 96))
    snake.draw(win)
    apple.draw(win)
    pygame.draw.lines(win, (0, 0, 0), True, [(10,10), (289,10), (289,289), (10,289)])
    pygame.display.update()


# main menu loop
def start_window(score):
    start = True
    pygame.init()

    start = Start(score)

    win = pygame.display.set_mode((WIN_HEIGHT,WIN_HEIGHT))
    clock = pygame.time.Clock()

    while start.running:
        clock.tick(15)
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                start.clickButton(mousePos)
                    
        start.draw_window_start(win,mousePos)

    pygame.quit()
    quit()


# actual game loop
def main():
    snake = Snake(150, 150)
    apple = Apple(snake.body)
    win = pygame.display.set_mode((WIN_HEIGHT,WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(10)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    snake.changeForce(key)

        # move snake
        snake.move()

        # check for apple, wall, body
        if snake.colApple(apple):
            apple = Apple(snake.body)
            score += 1
        elif snake.colWall():
            run = False
            start_window(score)
        elif snake.colBody():
            run = False
            start_window(score)

        # update screen
        draw_window_play(win, snake, apple)

    # quit the program
    pygame.quit()
    quit()


start_window(0)

