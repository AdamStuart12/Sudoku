import random

class Board:
    def __init__(self):
        self.solution = 0
        self.solved_boards = 0
        self.full_board = 0

    def generatePuzzle(self):
        board = [[0 for i in range(0,9)] for j in range(0,9)]
        self.generateFullBoard(board, 0, 0)
        print(f"#############\nFull board:\n{self.full_board}")

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

        validNumbers = sorted(validNumbers, key=lambda x: random.random())
        
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
        '''
        if not any("0" in row for row in board): # if no open spaces, solution is found
            self.solved_boards += 1
            if self.solved_boards == 1: # first solution found, save the solution
                self.solution = board
                return True
            else:
                raise DuplicateSolutionException() # more than one solution found therefore not valid
        '''

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
                print("NEW ROW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") # TODO remove
                validNums = []
                for x in range(0,9):
                    if board[y][x] == 0:
                        validNums.append(self.findValidNumbers(board, y, x))
                    else:
                        validNums.append([])
                    
                print(validNums) # TODO remove
                
                for x in range(0,9):
                    if len(validNums[x]) == 1: # there is only 1 possible number that can go in the tile
                        board[y][x] = validNums[x][0]
                        tileFound = True
                        print(f"Added: {validNums[x][0]} in row {y} column {x}") # TODO remove
            
                for num in range(1,10):
                    if sum(n.count(num) for n in validNums) == 1: # if number is only possible in 1 tile in row
                        for x in range(0,9): # find x position of tile
                            if num in validNums[x]:
                                board[y][x] = num
                                tileFound = True
                                print(f"Added: {num} in row {y} column {x}") # TODO remove
                print(board) # TODO remove

            print("FINISHED ROWS") # TODO remove


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
                                print(f"Added: {num} in row {y} column {x}") # TODO remove
                print(board) # TODO remove
            print("FINISHED COLUMNS") # TODO remove

            
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
                                    print(f"Added: {num} in row {(y*3)+i} column {(x*3)+j}") # TODO remove
                    print(board) # TODO remove

        # if here while loop has exited due to no tile being found, either board is solved or unsolvable
        if any(0 in row for row in board): # if 0 is still in board, it means there is no solution
            return False
        else:
            self.solution = board
            return True


    def getSolution(self):
        return self.solution

        #print(validNums)
            

board = [[6,8,0,0,0,7,1,0,0],
         [0,2,0,9,1,5,8,0,7],
         [9,0,0,6,0,3,5,2,0],
         [0,5,6,0,0,2,0,0,0],
         [3,0,0,0,0,0,0,0,0],
         [0,9,2,0,6,0,0,5,8],
         [7,0,0,0,5,6,0,8,1],
         [0,0,8,3,4,9,0,0,6],
         [0,0,0,8,0,1,4,3,0]]

board = [[0,0,0,4,0,9,8,0,2],
         [5,7,0,3,8,0,0,0,4],
         [0,0,0,0,0,2,5,0,0],
         [3,2,8,0,1,7,0,6,0],
         [0,5,7,9,3,0,0,0,0],
         [9,0,0,0,2,0,7,3,0],
         [7,8,0,1,0,0,0,0,0],
         [6,0,5,2,0,8,0,0,7],
         [0,9,4,0,7,3,0,5,0]]

temp = Board()
#validNumbers = temp.findValidNumbers(board,0,0)
#print(validNumbers)

#temp.solveSudoku(board,0,0)


#temp.humanSolve(board)
#human = temp.getSolution().copy()

temp.generatePuzzle()

#print(f"##################################\n SOLUTION:\n {temp.getSolution()}")

         
