import pygame as pyg
import math, random, time, sys
pyg.init()

run = True
score = 0
cur_block = next_block = None
gameover = False
input = True

# Game window
boardWidth = 300
boardHeight = 2*boardWidth
size = boardWidth//10
screenWidth = 2*boardWidth
screenHeight = boardHeight + 3*screenWidth//20
win = pyg.display.set_mode((screenWidth, screenHeight))
clock = pyg.time.Clock()

# Top left corner coordinates of board
board_x = size
board_y = 2*size

# Storing board grid
board_grid = []
for i in range(10):
    temp = []
    for j in range(24):
        temp.append([0, None])
    board_grid.append(temp)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
yellow = (255, 213, 0)
cyan = (0, 255, 255)
orange = (255, 150, 0)
purple = (255, 50, 255)

class tetromino:
    def __init__(self, id = None):
        # PARTS = x,y positions of the 4 blocks that make up each tetromino
        if id is None:
            # LOCATION IN NEXT BLOCK BOX
            random.seed()
            self.id = random.randrange(1, 8)
            # Cyan
            if self.id == 1:
                self.color = cyan
                self.parts = [[boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 4*size], 
                              [boardWidth + 7*size, board_y + 4*size]]
            # Blue
            elif self.id == 2:
                self.color = blue
                self.parts = [[boardWidth + 4*size, board_y + 3*size], 
                              [boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 4*size]]
            # Orange
            elif self.id == 3:
                self.color = orange
                self.parts = [[boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 3*size]]
            # Yellow
            elif self.id == 4:
                self.color = yellow
                self.parts = [[boardWidth + 4*size, board_y + 3*size], 
                              [boardWidth + 5*size, board_y + 3*size], 
                              [boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size]]
            # Green
            elif self.id == 5:
                self.color = green
                self.parts = [[boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 3*size], 
                              [boardWidth + 6*size, board_y + 3*size]]
            # Purple
            elif self.id == 6:
                self.color = purple
                self.parts = [[boardWidth + 4*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 4*size], 
                              [boardWidth + 5*size, board_y + 3*size]]
            # Red
            elif self.id == 7:
                self.color = red
                self.parts = [[boardWidth + 4*size, board_y + 3*size], 
                              [boardWidth + 5*size, board_y + 3*size], 
                              [boardWidth + 5*size, board_y + 4*size], 
                              [boardWidth + 6*size, board_y + 4*size]]
        else:
            # LOCATION IN BOARD
            self.id = id
            # Cyan
            if self.id == 1:
                self.color = cyan
                self.parts = [[4*size, board_y - size], 
                              [5*size, board_y - size], 
                              [6*size, board_y - size], 
                              [7*size, board_y - size]]
                self.rotation_point = [self.parts[2][0], self.parts[2][1] + size]
            # Blue
            elif self.id == 2:
                self.color = blue
                self.parts = [[5*size, board_y - size], 
                              [5*size, board_y], 
                              [6*size, board_y], 
                              [7*size, board_y]]
                self.rotation_point = [self.parts[2][0] + size//2, self.parts[2][1] + size//2]
            # Orange
            elif self.id == 3:
                self.color = orange
                self.parts = [[7*size, board_y - size], 
                              [7*size, board_y], 
                              [6*size, board_y], 
                              [5*size, board_y]]
                self.rotation_point = [self.parts[2][0] + size//2, self.parts[2][1] + size//2]
            # Yellow
            elif self.id == 4:
                self.color = yellow
                self.parts = [[5*size, board_y - size], 
                              [6*size, board_y - size], 
                              [5*size, board_y], 
                              [6*size, board_y]]
                self.rotation_point = [0, 0]
            # Green
            elif self.id == 5:
                self.color = green
                self.parts = [[5*size, board_y], 
                              [6*size, board_y], 
                              [6*size, board_y - size], 
                              [7*size, board_y - size]]
                self.rotation_point = [self.parts[1][0] + size//2, self.parts[1][1] + size//2]
            # Purple
            elif self.id == 6:
                self.color = purple
                self.parts = [[5*size, board_y], 
                              [6*size, board_y], 
                              [7*size, board_y], 
                              [6*size, board_y - size]]
                self.rotation_point = [self.parts[1][0], self.parts[1][1]]
            # Red
            elif self.id == 7:
                self.color = red
                self.parts = [[5*size, board_y - size], 
                              [6*size, board_y - size], 
                              [6*size, board_y], 
                              [7*size, board_y]]
                self.rotation_point = [self.parts[2][0] + size//2, self.parts[2][1] + size//2]
    
    # Converts X coordinate on window to X coordinate on board
    def convert_x(self, win_x):
        return (win_x - board_x)//size
    
    # Converts Y coordinate on window to Y coordinate on board
    def convert_y(self, win_y):
        return (board_y + boardHeight - win_y)//size
    
    def setBlock(self):
        global board_grid
        for i in range(4):
            x = self.convert_x(self.parts[i][0])
            y = self.convert_y(self.parts[i][1])
            board_grid[x][y] = [1, self.color]
    
    def moveLeft(self):
        global right_valid
        if left_valid:
            for i in range(4):
                self.parts[i][0] += -size
            self.rotation_point[0] += -size
            right_valid = True
    
    def moveRight(self):
        global left_valid
        if right_valid:
            for i in range(4):
                self.parts[i][0] += size
            self.rotation_point[0] += size
            left_valid = True
    
    def moveDown(self):
        for i in range(4):
            self.parts[i][1] += size
        self.rotation_point[1] += size
    
    # Checks if current block can move left
    def checkLeft(self):
        global left_valid
        con1 = con2 = False

        # Prevents current block from moving outside the left border of the board
        for i in range(4):
            if self.parts[i][0] <= board_x:
                con1 = True
                break
        
            # Checking if a block exists to the left of the current block
            x = self.convert_x(self.parts[i][0])
            y = self.convert_y(self.parts[i][1])
            
            # Exception caught if index out of bounds
            try:
                if x > 0 and board_grid[x - 1][y][0] != 0:
                    con2 = True
                    break
            except:
                con2 = True
        
        if con1 or con2:
            left_valid = False
        else:
            left_valid = True
    
    # Checks if current block can move right
    def checkRight(self):
        global right_valid
        con1 = con2 = False
        
        # Prevents current block from moving outside the right border of the board
        for i in range(4):
            if self.parts[i][0] >= boardWidth:
                con1 = True
                break
        
            # Checking if a block exists to the right of the current block
            x = self.convert_x(self.parts[i][0])
            y = self.convert_y(self.parts[i][1])
            
            # Exception caught if index out of bounds
            try:
                if x > 0 and board_grid[x + 1][y][0] != 0:
                    con2 = True
                    break
            except:
                con2 = True
        
        if con1 or con2:
            right_valid = False
        else:
            right_valid = True
    
    # Checks if current block can move down
    def checkDown(self):
        # Checking if a block exists underneath the current block
        for i in range(4):
            for x in range(10):
                for y in range(20):
                    if board_grid[x][y][0] != 0:
                        if self.parts[i][0] == board_x + x*size and self.parts[i][1] == board_y + boardHeight - y*size - size:
                            return True
        
        # Checking if the current block has reached the bottom of the board
        for i in range(4):
            if self.parts[i][1] == boardHeight + board_y - size:
                return True
        
        return False
    
    # Determines direction block is facing and applies rotation accordingly
    def rotate(self):
        # Cyan
        if self.id == 1:
            if self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][0] += 2*size
                self.parts[0][1] += -size
                self.parts[1][0] += size
                self.parts[2][1] += size
                self.parts[3][0] += -size
                self.parts[3][1] += 2*size
            elif self.rotation_point[0] <= self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][0] += size
                self.parts[0][1] += 2*size
                self.parts[1][1] += size
                self.parts[2][0] += -size
                self.parts[3][0] += -2*size
                self.parts[3][1] += -size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] <= self.parts[0][1]:
                self.parts[0][0] += -2*size
                self.parts[0][1] += size
                self.parts[1][0] += -size
                self.parts[2][1] += -size
                self.parts[3][0] += size
                self.parts[3][1] += -2*size
            elif self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][0] += -size
                self.parts[0][1] += -2*size
                self.parts[1][1] += -size
                self.parts[2][0] += size
                self.parts[3][0] += 2*size
                self.parts[3][1] += size
        # Blue
        elif self.id == 2:
            if self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][0] += 2*size
                self.parts[1][0] += size
                self.parts[1][1] += -size
                self.parts[3][0] += -size
                self.parts[3][1] += size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][1] += 2*size
                self.parts[1][0] += size
                self.parts[1][1] += size
                self.parts[3][0] += -size
                self.parts[3][1] += -size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][0] += -2*size
                self.parts[1][0] += -size
                self.parts[1][1] += size
                self.parts[3][0] += size
                self.parts[3][1] += -size
            elif self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][1] += -2*size
                self.parts[1][0] += -size
                self.parts[1][1] += -size
                self.parts[3][0] += size
                self.parts[3][1] += size
        # Orange
        elif self.id == 3:
            if self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][1] += 2*size
                self.parts[1][0] += -size
                self.parts[1][1] += size
                self.parts[3][0] += size
                self.parts[3][1] += -size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][0] += -2*size
                self.parts[1][0] += -size
                self.parts[1][1] += -size
                self.parts[3][0] += size
                self.parts[3][1] += size
            elif self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][1] += -2*size
                self.parts[1][0] += size
                self.parts[1][1] += -size
                self.parts[3][0] += -size
                self.parts[3][1] += size
            elif self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][0] += 2*size
                self.parts[1][0] += size
                self.parts[1][1] += size
                self.parts[3][0] += -size
                self.parts[3][1] += -size
        # Green
        elif self.id == 5:
            if self.rotation_point[0] < self.parts[3][0] and self.rotation_point[1] > self.parts[3][1]:
                self.parts[0][0] += size
                self.parts[0][1] += -size
                self.parts[2][0] += size
                self.parts[2][1] += size
                self.parts[3][1] += 2*size
            elif self.rotation_point[0] < self.parts[3][0] and self.rotation_point[1] < self.parts[3][1]:
                self.parts[0][0] += size
                self.parts[0][1] += size
                self.parts[2][0] += -size
                self.parts[2][1] += size
                self.parts[3][0] += -2*size
            elif self.rotation_point[0] > self.parts[3][0] and self.rotation_point[1] < self.parts[3][1]:
                self.parts[0][0] += -size
                self.parts[0][1] += size
                self.parts[2][0] += -size
                self.parts[2][1] += -size
                self.parts[3][1] += -2*size
            elif self.rotation_point[0] > self.parts[3][0] and self.rotation_point[1] > self.parts[3][1]:
                self.parts[0][0] += -size
                self.parts[0][1] += -size
                self.parts[2][0] += size
                self.parts[2][1] += -size
                self.parts[3][0] += 2*size
        # Purple
        elif self.id == 6:
            if self.rotation_point[0] == self.parts[3][0] and self.rotation_point[1] > self.parts[3][1]:
                self.parts[0][0] += size
                self.parts[0][1] += -size
                self.parts[2][0] += -size
                self.parts[2][1] += size
                self.parts[3][0] += size
                self.parts[3][1] += size
            elif self.rotation_point[0] < self.parts[3][0] and self.rotation_point[1] == self.parts[3][1]:
                self.parts[0][0] += size
                self.parts[0][1] += size
                self.parts[2][0] += -size
                self.parts[2][1] += -size
                self.parts[3][0] += -size
                self.parts[3][1] += size
            elif self.rotation_point[0] == self.parts[3][0] and self.rotation_point[1] < self.parts[3][1]:
                self.parts[0][0] += -size
                self.parts[0][1] += size
                self.parts[2][0] += size
                self.parts[2][1] += -size
                self.parts[3][0] += -size
                self.parts[3][1] += -size
            elif self.rotation_point[0] > self.parts[3][0] and self.rotation_point[1] == self.parts[3][1]:
                self.parts[0][0] += -size
                self.parts[0][1] += -size
                self.parts[2][0] += size
                self.parts[2][1] += size
                self.parts[3][0] += size
                self.parts[3][1] += -size
        # Red
        elif self.id == 7:
            if self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][0] += 2*size
                self.parts[1][0] += size
                self.parts[1][1] += size
                self.parts[3][0] += -size
                self.parts[3][1] += size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] > self.parts[0][1]:
                self.parts[0][1] += 2*size
                self.parts[1][0] += -size
                self.parts[1][1] += size
                self.parts[3][0] += -size
                self.parts[3][1] += -size
            elif self.rotation_point[0] < self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][0] += -2*size
                self.parts[1][0] += -size
                self.parts[1][1] += -size
                self.parts[3][0] += size
                self.parts[3][1] += -size
            elif self.rotation_point[0] > self.parts[0][0] and self.rotation_point[1] < self.parts[0][1]:
                self.parts[0][1] += -2*size
                self.parts[1][0] += size
                self.parts[1][1] += -size
                self.parts[3][0] += size
                self.parts[3][1] += size
    
    # Checks if rotation occurs out of bounds or on top of existing block
    def check_rotation(self):
        con1 = con2 = False
        
        # Checks if rotation occurs out of bounds
        for i in range(4):
            if self.parts[i][0] < board_x or self.parts[i][0] > boardWidth or self.parts[i][1] >= board_y + boardHeight:
                con1 = True
                break
        
        # Checks if rotation occurs on top of existing block
        for i in range(4):
            x = self.convert_x(self.parts[i][0])
            y = self.convert_y(self.parts[i][1])
            # Exception caught if index out of bounds
            try: 
                if board_grid[x][y][0] == 1:
                    con2 = True
                    break
            except:
                con2 = True
        
        # Undoes rotation
        if con1 or con2:
            self.rotate()
            self.rotate()
            self.rotate()
    
def clearLine():
    global board_grid, score
    for y in range(20):
        if y > 0:
            for x in range(10):
                if board_grid[x][y][0] == 1:
                    if x == 9:
                        score += 1
                        for i in range(10):
                            board_grid[i].pop(y)
                            board_grid[i].append([0, None])
                else:
                    break

def checkLose():
    global gameover, input
    for x in range(10):
        if board_grid[x][20][0] != 0:
            gameover = True
            input = False

# Generates text
def create_text(text, name, font_size, text_color, x, y):
    font = pyg.font.SysFont(name, font_size)
    ren = font.render(text, True, text_color)
    win.blit(ren, (x, y))

# Updates display    
def draw():
    pyg.display.set_caption("Tetris")
    win.fill(black)
    
    # Draws current tetromino
    for i in range(4):
        pyg.draw.rect(win, cur_block.color, (cur_block.parts[i][0], cur_block.parts[i][1], size, size))
    
    # Draws pieces in board
    for x in range(10):
        for y in range(20):
            if board_grid[x][y][0] != 0:
                pyg.draw.rect(win, board_grid[x][y][1], (x*size + board_x, board_y + boardHeight - y*size, size, size))
    
    # Board
    x = board_x
    y = board_y
    for i in range(boardHeight//size - 1):
        x += size
        y += size
        if x <= boardWidth:
            pyg.draw.line(win, white, (x, board_y), (x, board_y + boardHeight - 1))
        pyg.draw.line(win, white, (board_x, y), (board_x + boardWidth - 1, y))
    pyg.draw.rect(win, white, (board_x, board_y, boardWidth, boardHeight), width = 1)
    pyg.draw.rect(win, black, (board_x, 0, boardWidth, board_y)) 
    create_text("Rows: " + str(score), "Courier", board_x, white, board_x, board_y - board_x)
    
    # NEXT PIECE
    x = boardWidth + 2*size
    y = board_y + board_x
    w = screenWidth - boardWidth - 3*size
    h = w
    create_text("NEXT", "Courier", size, white, x, y - size)
    
    # Block
    for i in range(4):
        pyg.draw.rect(win, next_block.color, (next_block.parts[i][0], next_block.parts[i][1], size, size))
    
    # Border
    pyg.draw.rect(win, white, (x, y, w, h), width = 1)
    
    # Grid
    for i in range(h//size - 1):
        x += size
        y += size
        pyg.draw.line(win, black, (x, board_y + board_x), (x, board_y + board_x + h - 1))
        pyg.draw.line(win, black, (boardWidth + 2*board_x, y), (boardWidth + 2*board_x + w - 1, y))
    
    pyg.display.update()

def gameloop():
    global run, input, left_valid, right_valid, score, gameover, cur_block, next_block, board_grid
    next_block = tetromino()
    score = 0
    while run:
        cur_block = tetromino(next_block.id)
        next_block = tetromino()
        input = True
        left_valid = True
        right_valid = True
        
        # GAME OVER SCREEN
        while gameover:
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    run = False
                    gameover = False
                    pyg.quit()
                    sys.exit()
                if e.type == pyg.KEYDOWN:
                    if e.key == pyg.K_SPACE:
                        # Resetting board grid
                        board_grid = []
                        for i in range(10):
                            temp = []
                            for j in range(24):
                                temp.append([0, None])
                            board_grid.append(temp)
                        gameover = False
                        gameloop()
            create_text("GAME OVER", "Courier", size, white, 13*size - size//4, 12*size)
            create_text("Press SPACE to play again", "Courier", size//2, white, 12*size - size//4, 15*size)
            pyg.display.update()
        
        while input:
            clock.tick(5)
            for e in pyg.event.get():
                # Clicking X to quit
                if e.type == pyg.QUIT:
                    run = False
                    pyg.quit()
                    sys.exit()
                
                if e.type == pyg.KEYDOWN:
                    if e.key == pyg.K_SPACE:
                        while not cur_block.checkDown():
                            cur_block.moveDown()
                        cur_block.setBlock()
                        input = False
                    
                    elif e.key == pyg.K_UP:
                        cur_block.rotate()
                        cur_block.check_rotation()
                    
                    elif e.key == pyg.K_LEFT:
                        cur_block.checkLeft()
                        cur_block.moveLeft()
                        
                    elif e.key == pyg.K_RIGHT:
                        cur_block.checkRight()
                        cur_block.moveRight()
                        
                    elif e.key == pyg.K_DOWN:
                        if cur_block.checkDown():
                            cur_block.setBlock()
                            input = False
                        else:
                            cur_block.moveDown()
            
            if not cur_block.checkDown():
                cur_block.moveDown()
                #pyg.time.wait(150)
            else:
                cur_block.setBlock()
                input = False
            
            clearLine()
            checkLose()
            draw()

gameloop()
