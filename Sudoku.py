import random
import copy
import pygame

class App:
    def __init__(self):
        board_generator = Board()
        board = 0
        pygame.init()

        WINDOW_WIDTH = 1280
        WINDOW_HEIGHT = 720
        LIGHT_GRAY = (200, 200, 200)
        BORDER_GRAY = (160, 160, 160)
        WHITE = (255, 255, 255)

        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        pygame.display.set_caption("Sudoku")

        clock = pygame.time.Clock()
        FPS = 30

        board, images, image_rects, tile_colors = self.newPuzzle(0)
        '''
        image = pygame.image.load("1.png")
        image_rect = image.get_rect()
        image_rect.top = 100
        image_rect.left = 100
        tile_color = WHITE
        '''
        
        running = True

        while running:

            clock.tick(FPS)
          
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    #print("got here")
                    #sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    #if image_rect.collidepoint(mouse_pos):
                    #    print("hit")


            # DRAW EVERYTHING TO SCREEN
            window.fill(LIGHT_GRAY)
            ####
            
            #pygame.draw.rect(window, tile_color, tile)
            
            pygame.draw.rect(window, BORDER_GRAY, [90, 90, 520, 520], 0)
            
            for y in range(0,9):
                for x in range(0,9):
                    pygame.draw.rect(window, tile_colors[y][x], image_rects[y][x])
                    window.blit(images[y][x], image_rects[y][x])
            
            ##pygame.draw.rect(window, WHITE, image_rect)
            #window.blit(image, image_rect)
            pygame.display.flip()


    def newPuzzle(self, difficulty):
        TILE_WIDTH = 50
        if difficulty == 0:
            board = [[0 for i in range(0,9)] for j in range(0,9)]
        else:
            board = board_generator.generatePuzzle(difficulty)
        images = [[0 for i in range(0,9)] for j in range(0,9)]
        image_rects = [[0 for i in range(0,9)] for j in range(0,9)]
        tile_colors = [[0 for i in range(0,9)] for j in range(0,9)]
        
        for y in range(0,9):
            for x in range(0,9):
                if difficulty == 0:
                    images[y][x] = pygame.image.load("0.png")
                else:
                    pass
                    # TODO draw correct board
                image_rects[y][x] = images[y][x].get_rect()
                image_rects[y][x].top = (100 + (y*TILE_WIDTH) + (y*5) + ((y//3)*5))
                image_rects[y][x].left = (100 + (x*TILE_WIDTH) + (x*5) + ((x//3)*5))
                tile_colors[y][x] = (255, 255, 255)
                
        return board, images, image_rects, tile_colors

            

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
        
                
        return board
            

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
     
