import copy
import time

board = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]

class sudokuSolver():


    changeZeroInBox = False


    def printBoard(self):
        horizontalCounter = 0
        
        print ('-------------------------')
        
        for box in board:
            verticalCounter = 0
            
            print ('| ', end="")
            
            for number in box:
                print(number,'',end="")
                
                verticalCounter = verticalCounter + 1
                
                if verticalCounter == 3:
                    print ('| ',end="")
                    verticalCounter = 0
                    
            print('')
            horizontalCounter += 1
        
            if horizontalCounter == 3:
                print ('-------------------------')
                horizontalCounter = 0

    def searchForPossibleAnswer(self, board , line , number ):

        possibleNumbers = [1,2,3,4,5,6,7,8,9]
            
        for slot in range(0,9):
            if (board[line][slot] != 0 and possibleNumbers.count(board[line][slot]) == 1):
                possibleNumbers.remove(board[line][slot])

        for otherLine in range(0,9):
            if (board[otherLine][number] != 0 and possibleNumbers.count(board[otherLine][number]) == 1):
                possibleNumbers.remove(board[otherLine][number])

        if ( line <= 2):
            x = [0,1,2]
        elif (line <=5 and line >= 2):
            x = [3,4,5]
        else:
            x = [6,7,8]

        if ( number <= 2):
            y = [0,1,2]
        elif (number <=5 and number >= 2):
            y = [3,4,5]
        else:
            y = [6,7,8]

        for i in x:
            for j in y:
                if (board[i][j] != 0 and possibleNumbers.count(board[i][j]) == 1):
                    possibleNumbers.remove(board[i][j])

        if len(possibleNumbers) == 1:
            board[line][number] = possibleNumbers.pop(0)
            return [0]

        return possibleNumbers

    def assignThisValue(self, board, line, valueToFillIn):
        result = []


        for number in range(0,9):
            if (board[line][number] == 0):
                result = self.searchForPossibleAnswer(board, line, number)
                if result.count(valueToFillIn) == 1:
                    board[line][number] = valueToFillIn
                    break

    def checkRows(self,board):

        global changeZeroInBox
        possibleNumbers = [1,2,3,4,5,6,7,8,9]
        
        for number in range(0,9):
            result = []
            for line in range(0,9):
                if (board[line][number] == 0):
                    result = result + self.searchForPossibleAnswer(board,line,number)

            for n in range (1,9):
                if (result.count(n)== 1):
                    for line in range(0,9):
                        if board[line][number] == 0:
                            newResult = []
                            newResult = self.searchForPossibleAnswer(board, line, number)
                            if (newResult.count(n) == 1):
                                board[line][number] = n
                                changeZeroInBox = True
                
    def checkTheBoxes(self, board):
        self.checkTheBox(board, [0,1,2], [0,1,2])
        self.checkTheBox(board, [0,1,2], [3,4,5])
        self.checkTheBox(board, [0,1,2], [6,7,8])
        self.checkTheBox(board, [3,4,5], [0,1,2])
        self.checkTheBox(board, [3,4,5], [3,4,5])
        self.checkTheBox(board, [3,4,5], [6,7,8])
        self.checkTheBox(board, [6,7,8], [0,1,2])
        self.checkTheBox(board, [6,7,8], [3,4,5])
        self.checkTheBox(board, [6,7,8], [6,7,8])

    def checkTheBox(self, board, x, y):
        global changeZeroInBox
        result = []

        for i in x:
            for j in y:
                if (board[i][j] == 0):
                    result = result + self.searchForPossibleAnswer(board, i, j)

        
        for n in range (1,9):
            if result.count(n) == 1:
                for i in x:
                    for j in y:
                        if (board[i][j] == 0):
                            newResult = []
                            newResult = self.searchForPossibleAnswer(board, i, j)
                            if newResult.count(n) == 1:
                                board[i][j] = n
                                changeZeroInBox = True

    def scanForZero(self, board):
        global  changeZeroInBox
        
        didItFindAZero = False
        fillInAZero = True
        changeZeroInBox = False
        
        while (fillInAZero or changeZeroInBox):
            fillInAZero = False
            didItFindAZero = False
            for line in range(0,9):
                result = []
                for number in range(0,9):
                    if board[line][number] == 0:
                        result = result + self.searchForPossibleAnswer(board, line, number)
                        didItFindAZero = True
                        if (result.count(0) == 1):
                            fillInAZero = True
                for n in range (1,9):
                    if result.count(n) == 1:
                        self.assignThisValue(board, line, n)        


            changeZeroInBox = False
            self.checkRows(board)
            self.checkTheBoxes(board)


        return didItFindAZero

    def areThereZerosLeft(self):
        global board
        self.scanForZero(board)

        for line in range(0,9):
            for number in range(0,9):
                result = []
                if board[line][number] == 0:
                    result = result + self.searchForPossibleAnswer(board, line, number)
                for i in result:
                    tempBoard = []
                    tempBoard = copy.deepcopy(board)
                    board[line][number] = result.pop()
                    if( not self.scanForZero(board) ):
                        return
                    else:
                        board = copy.deepcopy(tempBoard)
                                

    def __init__(self, newBoard):
        self.board = newBoard
        self.printBoard()
        start_time = time.time()
        self.areThereZerosLeft()
        print("Finished in: " + str(time.time()-start_time) + " seconds")
        self.printBoard()

firstBoard = sudokuSolver(board)
