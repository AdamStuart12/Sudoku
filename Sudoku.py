class Board:
    def __init__(self):
        self.solution = 0
        self.solved_boards = 0

    def generateBoard(self):
        pass

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

    def getSolution(self):
        return self.solution
                                    

    def humanSolve(self, board):
        numAdded = True
        emptyExists = True
        while(numAdded and emptyExists):
            numAdded = False # if you go through the whole board without adding a number no solution exists
            emptyExists = False # tracks if an empty tile is found
            
            for y in range(0,9):
                for x in range(0,9):
                    if board[y][x] == 0: # loops through all empty tiles
                        emptyExists = True
                        validNumbers = self.findValidNumbers(board, y, x)
                        if len(validNumbers) == 1: # only 1 possible number in square so add it
                            board[y][x] = validNumbers[0]
                            print(board)
                            tileFound = True
                            
            if not emptyExists: # if no empty tiles were found, board is solved
                self.solution = board
                
        return False
            

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
temp.humanSolve(board)
print(f"##################################\n SOLUTION:\n {temp.getSolution()}")

         
