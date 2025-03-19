import random
import copy
import pygame
import string
import random
import time
import mysql.connector
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App:
    def __init__(self):

        ID = ""
        ID += random.choice(string.ascii_letters).lower()
        ID += random.choice(string.ascii_letters).lower()
        ID += str(random.randint(0,9))
        ID += str(random.randint(0,9))
        print(ID)
        
        pygame.init()
        pygame.font.init()

        # Variables / constants
        board_class = Board()
        WINDOW_WIDTH = 1130
        WINDOW_HEIGHT = 720
        LIGHT_GRAY = (200, 200, 200)
        BORDER_GRAY = (160, 160, 160)
        self.LIGHT_BLUE = (173, 216, 230)
        self.WHITE = (255, 255, 255)
        self.RED = (250, 127, 108)
        puzzle_font = pygame.font.SysFont('Calibri', 48)
        ID_font = pygame.font.SysFont('Calibri', 36, bold=True)
        difficulty = 3
        start = True
        completion_time = 0


        # Random Game Stuff
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku")

        clock = pygame.time.Clock()
        FPS = 30
        scene = "select"
        current_puzzle = 1
        self.start_time = 0
        self.end_time = 0

        # Buttons and game board
        board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles, number_counts = self.newPuzzle(difficulty)

        num_button_images = [[] for i in range(0,9)]
        num_button_rects = [[] for i in range(0,9)]
        for i in range(0,9):
            num_button_images[i] = pygame.transform.scale(pygame.image.load(resource_path(f"images/{i+1}.png")).convert_alpha(), (100,100))
            num_button_rects[i] = num_button_images[i].get_rect()
            num_button_rects[i].top = (190 + ((i//3)*(100+10)))
            num_button_rects[i].left = (700 + ((i%3)*(100+10)))

        
        rating_button_images = [[] for i in range(0,10)]
        rating_button_rects = [[] for i in range(0,10)]
        for i in range(0,10):
            rating_button_images[i] = pygame.image.load(resource_path(f"images/{i+1}.png"))
            rating_button_rects[i] = rating_button_images[i].get_rect()
            rating_button_rects[i].top = 380
            rating_button_rects[i].left = (225 + (i*50) + (i*20))

        new_puzzle_button_image = pygame.image.load(resource_path("images/new_puzzle_button.png"))
        new_puzzle_button_rect = new_puzzle_button_image.get_rect()
        new_puzzle_button_rect.top = 540
        new_puzzle_button_rect.left = 735

        # Gameloop
        running = True
        while running:

            clock.tick(FPS)
          
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if scene == "play":
                        # Board Clicked
                        for y in range(0,9):
                            for x in range(0,9):
                                if image_rects[y][x].collidepoint(mouse_pos):
                                    tile_colors = self.resetColors(tile_colors)
                                    if tile_colors[y][x] == self.WHITE:
                                        tile_colors[y][x] = self.LIGHT_BLUE
                                    sel_y = y
                                    sel_x = x

                        # Num Button Clicked
                        for i in range(0,9):
                        
                            if num_button_rects[i].collidepoint(mouse_pos):
                                top = image_rects[sel_y][sel_x].top
                                left = image_rects[sel_y][sel_x].left
                                
                                if board[sel_y][sel_x] == i+1: # if same number clicked
                                    images[sel_y][sel_x] = pygame.image.load(resource_path(f"images/0.png"))
                                    board[sel_y][sel_x] = 0
                                    tile_colors[sel_y][sel_x] = self.LIGHT_BLUE
                                    empty_tiles += 1
                                    number_counts[i] -= 1
                                    
                                else: # if different number clicked
                                    images[sel_y][sel_x] = pygame.image.load(resource_path(f"images/{i+1}.png"))
                                    board_val = board[sel_y][sel_x]

                                    # set selected tile to empty and find valid nums for that tile
                                    board[sel_y][sel_x] = 0
                                    valid_nums = board_class.findValidNumbers(board, sel_y, sel_x)
                                    board[sel_y][sel_x] = board_val

                                    # keep track of how many of each number is left to put on board
                                    if board_val != 0:
                                        number_counts[board_val-1] -= 1
                                    number_counts[i] += 1
                                    
                                    
                                    board[sel_y][sel_x] = i+1
                                    if (i+1) not in valid_nums:
                                        tile_colors[sel_y][sel_x] = self.RED
                                    else:
                                        tile_colors[sel_y][sel_x] = self.LIGHT_BLUE
                                    if board_val == 0:
                                        empty_tiles -= 1
                                        
                                image_rects[sel_y][sel_x] = images[sel_y][sel_x].get_rect()
                                image_rects[sel_y][sel_x].top = top
                                image_rects[sel_y][sel_x].left = left

                        if new_puzzle_button_rect.collidepoint(mouse_pos):
                            scene = "select"

                    if scene == "select":
                        for i in range(0,10):
                            if rating_button_rects[i].collidepoint(mouse_pos):
                                difficulty = i+1
                                board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles, number_counts = self.newPuzzle(difficulty)
                                completion_time = 0
                                scene = "play"


            if scene == "play":
                # DRAW EVERYTHING TO SCREEN
                window.fill(LIGHT_GRAY)
                ####
                
                #pygame.draw.rect(window, tile_color, tile)

                # Draws the board
                pygame.draw.rect(window, BORDER_GRAY, [90, 90, 520, 520], 0)
                for y in range(0,9):
                    for x in range(0,9):
                        pygame.draw.rect(window, tile_colors[y][x], image_rects[y][x])
                        window.blit(images[y][x], image_rects[y][x])

                # Draws the number buttons
                pygame.draw.rect(window, BORDER_GRAY, [690, 180, 340, 340], 0)
                for i in range(0,9):
                    
                    pygame.draw.rect(window, self.WHITE, num_button_rects[i])
                    if number_counts[i] < 9: # if you already have 9 of that number just show the white square
                        num_button_images[i].set_alpha(255)
                    else:
                        num_button_images[i].set_alpha(50)
                    window.blit(num_button_images[i], num_button_rects[i])
                # Draw new puzzle button
                window.blit(new_puzzle_button_image, new_puzzle_button_rect)
                
                # If puzzle is complete
                if empty_tiles == 0:
                    empty_tiles = -82
                    completion_time = int(time.time() - self.start_time)
                    
                # Draws win message if puzzle is complete
                if completion_time != 0:
                    curr_puzzle_text = puzzle_font.render(f"You win. Completion time {completion_time}s", False, (0, 0, 0))
                    window.blit(curr_puzzle_text, (90,40))
                    
                    
            if scene == "select":
                if start:
                    window.fill(LIGHT_GRAY)
                    start = False
                pygame.draw.rect(window, BORDER_GRAY, pygame.Rect(175, 190, 780, 300))
                for i in range(0,10):
                    pygame.draw.rect(window, self.WHITE, rating_button_rects[i])
                    window.blit(rating_button_images[i], rating_button_rects[i])
                line1 = puzzle_font.render(f"Chose puzzle difficulty", False, (0, 0, 0))
                line2 = puzzle_font.render("Where 1 is easy and 10 is difficult,", False, (0, 0, 0))
                window.blit(line1, (345,240))
                window.blit(line2, (235,290))
                
            
            pygame.display.flip()


    def newPuzzle(self, difficulty):
        board_generator = Board()
        self.WHITE = (255,255,255)
        self.LIGHT_BLUE = (173, 216, 230)
        TILE_WIDTH = 50
        sel_y = 0
        sel_x = 0
        completion_time = 0
        self.start_time = time.time()
        if difficulty == 0:
            board = [[0 for i in range(0,9)] for j in range(0,9)]
        else:
            board, empty_tiles = board_generator.generatePuzzle(difficulty)
        images = [[0 for i in range(0,9)] for j in range(0,9)]
        image_rects = [[0 for i in range(0,9)] for j in range(0,9)]
        tile_colors = [[self.WHITE for i in range(0,9)] for j in range(0,9)]
        tile_colors[0][0] = self.LIGHT_BLUE
        
        for y in range(0,9):
            for x in range(0,9):
                if difficulty == 0:
                    images[y][x] = pygame.image.load(resource_path("images/0.png"))
                else:
                    images[y][x] = pygame.image.load(resource_path(f"images/{board[y][x]}.png"))
                    image_rects[y][x] = images[y][x].get_rect()
                    image_rects[y][x].top = (100 + (y*TILE_WIDTH) + (y*5) + ((y//3)*5))
                    image_rects[y][x].left = (100 + (x*TILE_WIDTH) + (x*5) + ((x//3)*5))

        number_counts = [0,0,0,0,0,0,0,0,0]
        for row in board:
            for tile in row:
                if tile != 0:
                    number_counts[tile-1] += 1
                
        return board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles, number_counts


    def resetColors(self, tile_colors):
        for y in range(0,9):
            for x in range(0,9):
                if tile_colors[y][x] == self.LIGHT_BLUE:
                    tile_colors[y][x] = self.WHITE 
        return tile_colors


class Board:
    def __init__(self):
        self.solution = 0
        self.full_board = 0

    def generatePuzzle(self, difficulty):
        board = [[0 for i in range(0,9)] for j in range(0,9)]
        self.generateFullBoard(board, 0, 0)

        board = self.full_board.copy()

        # generate a list of all tile x and y positions, then randomly shuffle list
        cells = []
        for i in range(0,9):
            for j in range(0,9):
                cells.append([i,j])
        cells = sorted(cells, key=lambda x: random.random()) # randomly shuffles cells
        
        # remove the numers
        removed_numbers = 0
        
        if difficulty <= 7:
            removable_numbers = (difficulty*5)+5
        else:
            removable_numbers = (difficulty*10)+5

        for j in range(5):
            for i in range(len(cells)):
                if removed_numbers < removable_numbers: # used to limit number of removed numbers to set difficulty
                    cell_content = board[cells[i][0]][cells[i][1]]
                    if cell_content != 0:
                        board[cells[i][0]][cells[i][1]] = 0
                        if self.humanSolve(copy.deepcopy(board)) == False:
                            board[cells[i][0]][cells[i][1]] = cell_content # if board is not solvable, add number back
                        else: # it is now confirmed that the number is staying removed, so update tracking variable
                            removed_numbers += 1
                
        return board, removed_numbers
            

    def generateFullBoard(self, board, y, x):
        nextTile = self.choseTile(board, y, x)

        if nextTile == 0: # if no open spaces, board is fully generated
            self.full_board = board
            return True
        else:
            yn = nextTile[0]
            xn = nextTile[1]

        # open spaces found, continue solving
        validNumbers = self.findValidNumbers(board, yn, xn)
        if validNumbers == []: # open tile exists with no valid numbers, board is invalid
            return False

        # randomly shuffles the numbers
        validNumbers = sorted(validNumbers, key=lambda x: random.random()) 
        
        for number in validNumbers: # for each valid number, check if board has a solution
            board[yn][xn] = number
            if self.generateFullBoard(board, yn, xn):
                return True
            board[yn][xn] = 0
        return False


    def findValidNumbers(self, board, y, x):
        numbers = [1,2,3,4,5,6,7,8,9]
        
        #search the row
        for tile in board[y]:
            if tile in numbers:
                numbers.remove(tile)
        
        #search the column
        for row in board:
            if row[x] in numbers:
                numbers.remove(row[x])

        #search the square
        square = board[(y//3)*3:((y//3)*3)+3]
        square[0] = square[0][(x//3)*3:((x//3)*3)+3]
        square[1] = square[1][(x//3)*3:((x//3)*3)+3]
        square[2] = square[2][(x//3)*3:((x//3)*3)+3]

        for row in square:
            for tile in row:
                if tile in numbers:
                    numbers.remove(tile)

        return numbers
                

    def choseTile(self, board, y, x):
        for yn in range(y,9):
            for xn in range(x,9):
                if board[yn][xn] == 0:
                    return yn,xn
                
        for yn in range(0,9):
            for xn in range(0,9):
                if board[yn][xn] == 0:
                    return yn,xn

        return 0
                

    def solveSudoku(self, board, y, x):
        print(board)
        print("")
        nextTile = self.choseTile(board, y, x)

        if nextTile == 0: # if no open spaces, solution is found
            self.solution = board
            return True
        else:
            yn = nextTile[0]
            xn = nextTile[1]

        # open spaces found, continue solving
        validNumbers = self.findValidNumbers(board, yn, xn)
        if validNumbers == []: # open tile exists with no valid numbers, board is invalid
            return False
        
        for number in validNumbers:
            board[yn][xn] = number
            if self.solveSudoku(board, yn, xn):
                return True
            board[yn][xn] = 0
        return False
                                 

    def humanSolve(self, board):
        tileFound = True
        while(tileFound):
            tileFound = False


            for y in range(0,9): # for each tile
                
                validNums = []
                for x in range(0,9): # find valid numbers for each tile in the row
                    if board[y][x] == 0:
                        validNums = self.findValidNumbers(board, y, x)
        
                    if len(validNums) == 1: # there is only 1 possible number that can go in the tile
                        board[y][x] = validNums[0]
                        tileFound = True

            
            for y in range(0,9): # for each row
                
                validNums = []
                for x in range(0,9): # find valid numbers for each tile in the row
                    if board[y][x] == 0:
                        validNums.append(self.findValidNumbers(board, y, x))
                    else:
                        validNums.append([])
                
            
                for num in range(1,10):
                    if sum(n.count(num) for n in validNums) == 1: # if number is only valid in 1 tile in row
                        for x in range(0,9): # find x position of tile
                            if num in validNums[x]:
                                board[y][x] = num
                                tileFound = True


            for x in range(0,9): # for each column
                
                validNums = [] # find valid numbers for each tile in the column
                for y in range(0,9):
                    if board[y][x] == 0:
                        validNums.append(self.findValidNumbers(board, y, x))
                    else:
                        validNums.append([])

                for num in range(1,10):
                    if sum(n.count(num) for n in validNums) == 1: # if number is only valid in 1 tile in column
                        for y in range(0,9): # find y position of tile
                            if num in validNums[y]:
                                board[y][x] = num
                                tileFound = True


            
            for y in range(0,3): # for each 3x3 square
                for x in range(0,3):
                    validNums = []
                    for i in range(0,3): # for each tile in the 3x3 square
                        for j in range(0,3):
                            if board[(y*3)+i][(x*3)+j] == 0:
                                validNums.append(self.findValidNumbers(board, (y*3)+i, (x*3)+j))
                            else:
                                validNums.append([])

                    for num in range(1,10):
                        if sum(n.count(num) for n in validNums) == 1: # if number is only valid in 1 tile in 3x3
                            for n in range(0,9): # find positioni of tile in validNums
                                if num in validNums[n]:
                                    i = (n//3) # i and j are the positions of the tile within the 3x3 grid
                                    j = (n%3) # this finds these from the 1d array validNums
                                    board[(y*3)+i][(x*3)+j] = num
                                    tileFound = True

        # if here while loop has exited due to no tile being found, either board is solved or unsolvable
        if any(0 in row for row in board): # if 0 is still in board, it means there is no solution
            return False
        else:
            self.solution = board
            return True


    def getSolution(self):
        return self.solution
            

board = [[0,0,0,4,0,9,8,0,2],
         [5,7,0,3,8,0,0,0,4],
         [0,0,0,0,0,2,5,0,0],
         [3,2,8,0,1,7,0,6,0],
         [0,5,7,9,3,0,0,0,0],
         [9,0,0,0,2,0,7,3,0],
         [7,8,0,1,0,0,0,0,0],
         [6,0,5,2,0,8,0,0,7],
         [0,9,4,0,7,3,0,5,0]]


#temp = Board()
#validNumbers = temp.findValidNumbers(board,0,0)
#print(validNumbers)

#temp.solveSudoku(board,0,0)


#temp.humanSolve(board)
#human = temp.getSolution().copy()

#temp.generatePuzzle()

#print(f"##################################\n SOLUTION:\n {temp.getSolution()}")

if __name__ == "__main__":
    app = App()
    #print("here")
    #temp = Board()
    #board = temp.generatePuzzle(10)
    #print(board)
     
