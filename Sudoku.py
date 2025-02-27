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
        WINDOW_WIDTH = 1280
        WINDOW_HEIGHT = 720
        LIGHT_GRAY = (200, 200, 200)
        BORDER_GRAY = (160, 160, 160)
        self.LIGHT_BLUE = (173, 216, 230)
        self.WHITE = (255, 255, 255)
        self.RED = (250, 127, 108)
        puzzle_font = pygame.font.SysFont('Calibri', 48)
        ID_font = pygame.font.SysFont('Calibri', 36, bold=True)
        results = [0,0,0]
        times = [0,0,0]
        difficulty = 3
        actuals = [0,0,0]


        # Random Game Stuff
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku")

        clock = pygame.time.Clock()
        FPS = 30
        scene = "start"
        current_puzzle = 1
        self.start_time = 0
        self.end_time = 0

        # Buttons and game board
        board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles = self.newPuzzle(difficulty)

        num_button_images = [[] for i in range(0,9)]
        num_button_rects = [[] for i in range(0,9)]
        for i in range(0,9):
            num_button_images[i] = pygame.image.load(resource_path(f"{i+1}_button.png"))
            num_button_rects[i] = num_button_images[i].get_rect()
            num_button_rects[i].top = (190 + ((i//3)*(100+10)))
            num_button_rects[i].left = (700 + ((i%3)*(100+10)))

        quit_button_image = pygame.image.load(resource_path("quit.png"))
        quit_button_rect = quit_button_image.get_rect()
        quit_button_rect.top = 660
        quit_button_rect.left = 1040

        skip_button_image = pygame.image.load(resource_path("skip.png"))
        skip_button_rect = skip_button_image.get_rect()
        skip_button_rect.top = 620
        skip_button_rect.left = 90

        quit_prompt_image = pygame.image.load(resource_path("quit_prompt.png"))
        quit_prompt_rect = quit_prompt_image.get_rect()
        quit_prompt_rect.top = 210
        quit_prompt_rect.left = 440

        skip_prompt_image = pygame.image.load(resource_path("skip_prompt.png"))
        skip_prompt_rect = skip_prompt_image.get_rect()
        skip_prompt_rect.top = 210
        skip_prompt_rect.left = 440

        quit_yes_image = pygame.image.load(resource_path("yes.png"))
        quit_yes_rect = quit_yes_image.get_rect()
        quit_yes_rect.top = 400
        quit_yes_rect.left = 470

        quit_no_image = pygame.image.load(resource_path("no.png"))
        quit_no_rect = quit_no_image.get_rect()
        quit_no_rect.top = 400
        quit_no_rect.left = 650

        rating_button_images = [[] for i in range(0,10)]
        rating_button_rects = [[] for i in range(0,10)]
        for i in range(0,10):
            rating_button_images[i] = pygame.image.load(resource_path(f"{i+1}_button.png"))
            rating_button_rects[i] = rating_button_images[i].get_rect()
            rating_button_rects[i].top = 400
            rating_button_rects[i].left = (50 + (i*100) + (i*20))

        start_button_image = pygame.image.load(resource_path("start.png"))
        start_button_rect = start_button_image.get_rect()
        start_button_rect.top = 500
        start_button_rect.left = 560

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
                                    if tile_colors[y][x] == self.WHITE:
                                        tile_colors = self.resetColors(tile_colors)
                                        tile_colors[y][x] = self.LIGHT_BLUE
                                        sel_y = y
                                        sel_x = x

                        # Num Button Clicked
                        for i in range(0,9):
                            if num_button_rects[i].collidepoint(mouse_pos):
                                top = image_rects[sel_y][sel_x].top
                                left = image_rects[sel_y][sel_x].left
                                
                                if board[sel_y][sel_x] == i+1: # if same number clicked
                                    images[sel_y][sel_x] = pygame.image.load(resource_path(f"0.png"))
                                    board[sel_y][sel_x] = 0
                                    tile_colors[sel_y][sel_x] = self.LIGHT_BLUE
                                    empty_tiles += 1
                                    
                                else: # if different number clicked
                                    images[sel_y][sel_x] = pygame.image.load(resource_path(f"{i+1}.png"))
                                    valid_nums = board_class.findValidNumbers(board, sel_y, sel_x)
                                    board_val = board[sel_y][sel_x]
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

                        if quit_button_rect.collidepoint(mouse_pos):
                            scene = "quit_prompt"

                        if skip_button_rect.collidepoint(mouse_pos):
                            scene = "skip_prompt"

                    if scene == "quit_prompt":
                        if quit_no_rect.collidepoint(mouse_pos):
                            scene = "play"
                        if quit_yes_rect.collidepoint(mouse_pos):
                            scene = "finished_incomplete"

                    if scene == "skip_prompt":
                        if quit_no_rect.collidepoint(mouse_pos):
                            scene = "play"
                        if quit_yes_rect.collidepoint(mouse_pos):
                            results[current_puzzle-1] = 0
                            times[current_puzzle-1] = 0
                            actuals[current_puzzle-1] = difficulty
                            if current_puzzle == 3:
                                    mydb = mysql.connector.connect(
                                      host="132.145.18.222",
                                      user="acs2000",
                                      password="wnd4VKSANY3",
                                      database="acs2000"
                                    )
                                    SQL = f"INSERT INTO Study VALUES ('{ID}', {results[0]}, {results[1]}, {results[2]});"
                                    SQL2 = f"INSERT INTO Times VALUES ('{ID}', {times[0]}, {times[1]}, {times[2]});"
                                    SQL3 = f"INSERT INTO Actuals VALUES ('{ID}', {actuals[0]}, {actuals[1]}, {actuals[2]});"
                                    db = mydb.cursor()
                                    db.execute(SQL)
                                    mydb.commit()
                                    db.execute(SQL2)
                                    mydb.commit()
                                    db.execute(SQL3)
                                    mydb.commit()
                                    scene = "finished_success"
                            
                            else:
                                if difficulty != 1:
                                    difficulty -= 1
                                board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles = self.newPuzzle(difficulty)
                                scene = "play"
                                current_puzzle += 1

                    if scene == "win":
                        for i in range(0,10):
                            if rating_button_rects[i].collidepoint(mouse_pos):
                                results[current_puzzle-1] = i+1
                                actuals[current_puzzle-1] = difficulty
                                print(results)
                                print(actuals)
                                
                                
                                if current_puzzle == 3:
                                    mydb = mysql.connector.connect(
                                      host="132.145.18.222",
                                      user="acs2000",
                                      password="wnd4VKSANY3",
                                      database="acs2000"
                                    )
                                    SQL = f"INSERT INTO Study VALUES ('{ID}', {results[0]}, {results[1]}, {results[2]});"
                                    SQL2 = f"INSERT INTO Times VALUES ('{ID}', {times[0]}, {times[1]}, {times[2]});"
                                    SQL3 = f"INSERT INTO Actuals VALUES ('{ID}', {actuals[0]}, {actuals[1]}, {actuals[2]});"
                                    db = mydb.cursor()
                                    db.execute(SQL)
                                    mydb.commit()
                                    db.execute(SQL2)
                                    mydb.commit()
                                    db.execute(SQL3)
                                    mydb.commit()
                                    scene = "finished_success"
                                else:
                                    chosen = i+1
                                    if chosen <= (difficulty+3):
                                        difficulty += 2
                                        if difficulty > 10:
                                            difficulty -= difficulty % 10
                                    elif chosen >= difficulty+4:
                                        if difficulty != 1:
                                            difficulty -= 1
                                    print(f"difficulty: {difficulty}")
                                    board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles = self.newPuzzle(difficulty)
                                    scene = "play"
                                    current_puzzle += 1

                    if scene == "start":
                        if start_button_rect.collidepoint(mouse_pos):
                            print("start pressed")
                            scene = "play"


            if scene == "start":
                window.fill(LIGHT_GRAY)
                line1 = puzzle_font.render("Welcome!", False, (0, 0, 0))
                line2 = puzzle_font.render(f"Your ID is {ID}, please make a note of this", False, (0, 0, 0))
                line3 = puzzle_font.render("Your task is to solve 3 sudoku puzzles", False, (0, 0, 0))
                line4 = puzzle_font.render("After each puzzle you will be asked to rate the difficulty", False, (0, 0, 0))
                line5 = puzzle_font.render(f"Every puzzle is solvable by a human", False, (0, 0, 0))
                line6 = puzzle_font.render(f"Press the button below when you are ready to begin", False, (0, 0, 0))
                window.blit(line1, (530,110))
                window.blit(line2, (230,160))
                window.blit(line3, (280,210))
                window.blit(line4, (100,260))
                window.blit(line5, (300,310))
                window.blit(line6, (130,360))
                window.blit(start_button_image, start_button_rect)

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
                    window.blit(num_button_images[i], num_button_rects[i])

                # Draws misc buttons and text
                window.blit(quit_button_image, quit_button_rect)
                window.blit(skip_button_image, skip_button_rect)
                curr_puzzle_text = puzzle_font.render(f"Puzzle {current_puzzle} out of 3", False, (0, 0, 0))
                window.blit(curr_puzzle_text, (90,40))
                ID_text = ID_font.render(f"Your ID: {ID}", False, (0, 0, 0))
                window.blit(ID_text, (1060,625))

                if empty_tiles == 0:
                    time.sleep(0.2)
                    scene = "win"
                    self.end_time = time.time()
                    times[current_puzzle-1] = self.end_time - self.start_time
                    print(times)
                    
                    

            if scene == "win":
                window.fill(LIGHT_GRAY)
                for i in range(0,10):
                    pygame.draw.rect(window, self.WHITE, rating_button_rects[i])
                    window.blit(rating_button_images[i], rating_button_rects[i])
                line1 = puzzle_font.render(f"You have completed puzzle {current_puzzle}", False, (0, 0, 0))
                line2 = puzzle_font.render("Where 1 is extremely easy and 10 is extremely difficult,", False, (0, 0, 0))
                line3 = puzzle_font.render("how difficult did you find that puzzle?", False, (0, 0, 0))
                window.blit(line1, (350,210))
                window.blit(line2, (105,260))
                window.blit(line3, (280,310))

            if scene == "finished_success":
                window.fill(LIGHT_GRAY)
                line1 = puzzle_font.render("You have completed the 3 required puzzles", False, (0, 0, 0))
                line2 = puzzle_font.render(f"Your ID is {ID}, please make a note of this", False, (0, 0, 0))
                line3 = puzzle_font.render("You can now close this app and move on to the questionnaire", False, (0, 0, 0))
                window.blit(line1, (230,260))
                window.blit(line2, (250,310))
                window.blit(line3, (50,360))

            if scene == "finished_incomplete":
                window.fill(LIGHT_GRAY)
                line1 = puzzle_font.render("You have chosen to end your participation in the study", False, (0, 0, 0))
                line2 = puzzle_font.render("Any information held about you will be deleted", False, (0, 0, 0))
                line3 = puzzle_font.render("Thank you for your time", False, (0, 0, 0))
                window.blit(line1, (115,260))
                window.blit(line2, (200,310))
                window.blit(line3, (400,360))
                #window.blit(finished_incomplete_image, finished_incomplete_rect)

            if scene == "quit_prompt":
                window.blit(quit_prompt_image, quit_prompt_rect)
                window.blit(quit_yes_image, quit_yes_rect)
                window.blit(quit_no_image, quit_no_rect)

            if scene == "skip_prompt":
                window.blit(skip_prompt_image, skip_prompt_rect)
                window.blit(quit_yes_image, quit_yes_rect)
                window.blit(quit_no_image, quit_no_rect)
                
                

            
            ##pygame.draw.rect(window, WHITE, image_rect)
            #window.blit(image, image_rect)
            pygame.display.flip()


    def newPuzzle(self, difficulty):
        board_generator = Board()
        self.WHITE = (255,255,255)
        self.LIGHT_BLUE = (173, 216, 230)
        TILE_WIDTH = 50
        sel_y = 0
        sel_x = 0
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
                    images[y][x] = pygame.image.load(resource_path("0.png"))
                else:
                    images[y][x] = pygame.image.load(resource_path(f"{board[y][x]}.png"))
                    image_rects[y][x] = images[y][x].get_rect()
                    image_rects[y][x].top = (100 + (y*TILE_WIDTH) + (y*5) + ((y//3)*5))
                    image_rects[y][x].left = (100 + (x*TILE_WIDTH) + (x*5) + ((x//3)*5))
                
        return board, images, image_rects, tile_colors, sel_y, sel_x, empty_tiles


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
        #print(f"#############\nFull board:\n{self.full_board}") # TODO remove

        board = self.full_board.copy()

        
        cells = []
        for i in range(0,9):
            for j in range(0,9):
                cells.append([i,j])
        cells = sorted(cells, key=lambda x: random.random()) # randomly shuffles cells
        

        removed_numbers = 0
        for i in range(len(cells)):
            if removed_numbers < (difficulty*5)+11: # used to limit number of removed numbers to set difficulty
                cell_content = board[cells[i][0]][cells[i][1]]
                board[cells[i][0]][cells[i][1]] = 0
                #print(board)
                #print(self.humanSolve(copy.deepcopy(board)))
                if self.humanSolve(copy.deepcopy(board)) == False:
                    #print("got here")
                    board[cells[i][0]][cells[i][1]] = cell_content # if board with number removed is not solvable, add the number back
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

        validNumbers = sorted(validNumbers, key=lambda x: random.random()) # randomly shuffles the numbers
        
        for number in validNumbers:
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
            for y in range(0,9): # for each row
                #print("NEW ROW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") # TODO remove
                validNums = []
                for x in range(0,9):
                    if board[y][x] == 0:
                        validNums.append(self.findValidNumbers(board, y, x))
                    else:
                        validNums.append([])
                    
                #print(validNums) # TODO remove
                
                for x in range(0,9):
                    if len(validNums[x]) == 1: # there is only 1 possible number that can go in the tile
                        board[y][x] = validNums[x][0]
                        tileFound = True
                        #print(f"Added: {validNums[x][0]} in row {y} column {x}") # TODO remove
            
                for num in range(1,10):
                    if sum(n.count(num) for n in validNums) == 1: # if number is only possible in 1 tile in row
                        for x in range(0,9): # find x position of tile
                            if num in validNums[x]:
                                board[y][x] = num
                                tileFound = True
                                #print(f"Added: {num} in row {y} column {x}") # TODO remove
                #print(board) # TODO remove

            #print("FINISHED ROWS") # TODO remove


            for x in range(0,9): # for each column
                
                validNums = []
                for y in range(0,9):
                    if board[y][x] == 0:
                        validNums.append(self.findValidNumbers(board, y, x))
                    else:
                        validNums.append([])

                for num in range(1,10):
                    if sum(n.count(num) for n in validNums) == 1: # if number is only possible in 1 tile in column
                        for y in range(0,9): # find y position of tile
                            if num in validNums[y]:
                                board[y][x] = num
                                tileFound = True
                                #print(f"Added: {num} in row {y} column {x}") # TODO remove
                #print(board) # TODO remove
            #print("FINISHED COLUMNS") # TODO remove

            
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
                        if sum(n.count(num) for n in validNums) == 1: # if number is only possible in 1 tile in 3x3 square
                            for n in range(0,9): # find positioni of tile in validNums
                                if num in validNums[n]:
                                    i = (n//3) # i and j are the positions of the tile within the 3x3 grid
                                    j = (n%3) # this finds these from the 1d array validNums
                                    board[(y*3)+i][(x*3)+j] = num
                                    tileFound = True
                                    #print(f"Added: {num} in row {(y*3)+i} column {(x*3)+j}") # TODO remove
                    #print(board) # TODO remove

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
     
