import util, copy
from board import *
from pieceGenerator import *
from config import *

class Extractor:


    def getAdjacentSpaces(self, space, board):
        spaceList = []
        x, y  = space
        if x + 1 < board.height:
            spaceList.append((x + 1, y))
            # if y + 1 <= board.width:
            #     spaceList.append((x+1, y+1))
            # if y - 1 >= 0:
            #     spaceList.append((x+1, y-1))
        if x - 1 >= 0:
            spaceList.append((x-1, y))
            # if y + 1 <= board.width:
            #     spaceList.append((x-1, y+1))
            # if y - 1 >= 0:
            #     spaceList.append((x-1, y-1))

        if y + 1 < board.width:
            spaceList.append((x, y+1))
        if y - 1 >= 0:
            spaceList.append((x, y-1))
        return spaceList

    def getHolesSizeSquared(self, blankSpaceSet, board):
        
        if len(blankSpaceSet) == 0:
            return 0

        space = blankSpaceSet.pop()
        blankSpaceSet.add(space)
        visited = set()
        sumSquaredHoleSize = 0
        for space in blankSpaceSet:
            sumSquaredHoleSize += (self.getHolesUtil(blankSpaceSet, board, visited, space, 0))**2
        return sumSquaredHoleSize

    def getHolesUtil(self, blankSpaceSet, board, visited, space, countHoleSize):
        topLineTemp = board.getTopLine(normalize=False)
        visited.add(space)
        adjSpaces = self.getAdjacentSpaces(space, board)
        for adjspace in adjSpaces:
            y, x = adjspace
            y1, x1 = topLineTemp[x]
            if y > y1:
                continue
            print y, x
            if board.board[x][y] == BLANK and adjspace not in visited:
                print "hi"
                countHoleSize += 1
                self.getHolesUtil(blankSpaceSet, board, visited, adjspace, countHoleSize)
        print countHoleSize
        return countHoleSize
        



    def getFeatures(self, state, action):
        features = util.Counter()
        # features will be
        # 1. number of lines we will clear by taking the action
        # 2. difference between height of adjacent columns on the board
        # 3. highest point in board
        # 4. total holes in board
        # since state also includes the next piece, we may be able to take this a step further
        # to do this, we will first create a new board (a copy) so we do not edit the board object we are given directly.
        # 1. addToBoard(board, fallingpiece) - this edits the board directly
        # 2. removeCompleteLines(board) - this returns the number of lines that we remove
        # 3. we will now have an edited board, so we can easily calculate the bumpiness, highest point, total holes

        #difference between height of adjacent columns on the board (average height):
        features["bias"] = 0.1

        oldboard = state[0]
        newBoard = copy.deepcopy(oldboard)
        board = Board(len(newBoard), len(newBoard[0]), newBoard)
        piece = state[1]
        pG = PieceGenerator()
        currPiece = pG.genPiece(piece.shape, piece.rotation)

        currPiece.setAction(action)

        board.addToBoard(currPiece)

        numLinesRemoved = board.removeCompleteLines()
        # features["numLinesRemoved"] = numLinesRemoved

        topLine = board.getTopLine(normalize=False)
        avgHeightDiff = 0
        # BOARD STORES HIGHEST POINT AS BOTTOM, LOWEST POINT AS TOP
        # SO FINDING THIS HIGHEST POINT IS REVERSED
        highestPoint = float('inf')
        for i in range(len(topLine)):
            if topLine[i][0] < highestPoint:
                highestPoint = topLine[i][0]
            curHeight = topLine[i][0]
            if i + 1 < len(topLine) and i - 1 >= 0:
                rightHeight = topLine[i + 1][0]
                leftHeight = topLine[i - 1][0]
                avgHeightDiff += (abs(rightHeight - curHeight) + abs(leftHeight - curHeight))/2
            elif i + 1 >= len(topLine) and i - 1 >= 0:
                leftHeight = topLine[i - 1][0]
                avgHeightDiff += abs(leftHeight - curHeight)
            elif i - 1 < 0 and i + 1 < len(topLine):
                rightHeight = topLine[i + 1][0]
                avgHeightDiff += abs(rightHeight - curHeight)
        avgHeightDiff = float(avgHeightDiff)/len(topLine)
        features["avgHeightDiff"] = avgHeightDiff / (float(board.height) * 10)
        features["highestPoint"] = (board.height - highestPoint - 1) / (float(board.height) * 10)


        blankSpaceSet = set()
        numHoles = 0
        for column in range(len(board.board)):
            col = board.board[column]
            index = None
            for i in range(len(col)):
                if col[i] != BLANK:
                    index = i
                    break

            if index is not None:
                for n in range(index, len(col)):
                    if col[n] == BLANK:
                        # blankSpaceSet.append((n, column))
                        #print str(n) + str(column)
                        coordinates = (n, column)
                        blankSpaceSet.add(coordinates)
                        #print blankSpaceSet
                        numHoles += 1
        features["numHoles"] = numHoles / (float(board.width * board.height) * 10)

        
        # blankSpaceSet = set()
        # for col in range(len(board)):
        #     for i in range(len(col)):
        #         if board[col][i] == BLANK:
        #             coordinates = (i, col)
        #             blankSpaceSet.add(coordinates)

        # blankSpaceSet = set()
        # depth = board.height
        # for i in range(len(topLine)):
        #     y = topLine[i][0]
        #     for n in range(y, depth - 1):
        #         if board.board[n][i] == BLANK:
        #             coordinates = (n, i)
        #             blankSpaceSet.add(coordinates)

        holeSizeSquared = self.getHolesSizeSquared(blankSpaceSet, board)
        features["holeSizeSquared"] = holeSizeSquared

        return features


         #just make new board
