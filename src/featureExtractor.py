import util, copy
from board import *
from pieceGenerator import *
from config import *

class Extractor:
    def __init__(self):
        self.pG = PieceGenerator()

    def getAdjacentSpaces(self, space, board):
        spaceList = []
        row, col  = space
        if row + 1 < board.height:
            spaceList.append((row + 1, col))
        if row - 1 >= 0:
            spaceList.append((row - 1, col))
        if col + 1 < board.width:
            spaceList.append((row, col + 1))
        if col - 1 >= 0:
            spaceList.append((row, col - 1))
        return spaceList

    def getHolesUtil(self, start, board, topLine, visited):
        holes = 0
        stack = [start]
        while stack:
            space = stack.pop()
            visited.add(space)
            holes += 1
            frontier = self.getAdjacentSpaces(space, board)
            for adjSpace in frontier:
                if adjSpace not in visited:
                    row, col = adjSpace
                    topRow, topCol = topLine[col]
                    if row > topRow and board.board[col][row] == BLANK:
                        stack.append(adjSpace)
        return holes

    def getHolesSizeSquared(self, blankSpaceSet, board, topLine):
        if len(blankSpaceSet) == 0:
            return 0
        visited = set()
        sumSquares = 0
        for space in blankSpaceSet:
            if space not in visited:
                holes = self.getHolesUtil(space, board, topLine, visited)
                sumSquares += holes ** 2
        return sumSquares

    def getAggregateHeight(self, topLine, height):
        agHeight = 0
        for row, _ in topLine:
            h = height - row - 1
            agHeight += h
        return agHeight

    def getHighestPoint(self, topLine, height):
        highestPoint = float('inf')
        for i in range(len(topLine)):
            if topLine[i][0] < highestPoint:
                highestPoint = topLine[i][0]
        return height - highestPoint - 1

    def getAvgHeightDiff(self, topLine):
        totalHeightDiff = 0
        for i in range(len(topLine)):
            curHeight = topLine[i][0]
            if i + 1 < len(topLine) and i - 1 >= 0:
                rightHeight = topLine[i + 1][0]
                leftHeight = topLine[i - 1][0]
                totalHeightDiff += (abs(rightHeight - curHeight) + abs(leftHeight - curHeight))/2
            elif i + 1 >= len(topLine) and i - 1 >= 0:
                leftHeight = topLine[i - 1][0]
                totalHeightDiff += abs(leftHeight - curHeight)
            elif i - 1 < 0 and i + 1 < len(topLine):
                rightHeight = topLine[i + 1][0]
                totalHeightDiff += abs(rightHeight - curHeight)
        return totalHeightDiff / float(len(topLine))

    def getHoles(self, board):
        blankSpaceSet = set()
        for column in range(len(board)):
            col = board[column]
            index = None
            for i in range(len(col)):
                if col[i] != BLANK:
                    index = i
                    break
            if index is not None:
                for n in range(index, len(col)):
                    if col[n] == BLANK:
                        coordinates = (n, column)
                        blankSpaceSet.add(coordinates)
        return blankSpaceSet

    def takeAction(self, state, action):
        oldboard, piece, nextPiece = state
        newBoard = copy.deepcopy(oldboard)
        board = Board(len(newBoard), len(newBoard[0]), newBoard)
        currPiece = self.pG.genRandPieceFromShape(piece)

        currPiece.setAction(action)
        board.addToBoard(currPiece)

        return board, currPiece

    def getGreedyFeatures(self, state, action):
        board, currPiece = self.takeAction(state, action)
        return board.removeCompleteLines(), len(self.getHoles(board.board))

    def getFeatures(self, state, action):
        features = util.Counter()

        features["bias"] = 1.0

        board, currPiece = self.takeAction(state, action)

        numLinesRemoved = board.removeCompleteLines()
        # features["numLinesRemoved"] = numLinesRemoved

        topLine = board.getTopLine(normalize=False)
        features["aggregateHeight"] = self.getAggregateHeight(topLine, board.height)
        # features["highestPoint"] = self.getHighestPoint(topLine, board.height)
        features["avgHeightDiff"] = self.getAvgHeightDiff(topLine)

        blankSpaceSet = self.getHoles(board.board)
        # features["numHoles"] = len(blankSpaceSet)

        holeSizeSquared = self.getHolesSizeSquared(blankSpaceSet, board, topLine)
        features["holeSizeSquared"] = holeSizeSquared / float(board.width * board.height)

        features.divideAll(float(board.width * board.height))

        return features
