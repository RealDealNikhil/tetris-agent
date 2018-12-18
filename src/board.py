from config import *
from pieceGenerator import *

class Board:
    def __init__(self, width, height, board=None):
        self.width = width
        self.height = height
        self.generator= PieceGenerator()
        if board is None:
            self.board = self.getBlankBoard()
        else:
            self.board = board

    def getBlankBoard(self):
        # create and return a new blank board data structure
        board = []
        for i in range(self.width):
            board.append([BLANK] * self.height)
        return board

    # for every rotation, check which columns we can drop the piece down
    def getLegalActions(self, piece):
        actions = []
        rotations = piece.getRotations()
        for r in range(rotations):
            testPiece = self.generator.genPiece(piece.shape, r)
            xLOffset, xROffset, yOffset = testPiece.getOffsets()
            testPiece.setY(0)
            for x in range(0 - xLOffset, self.width):
                testPiece.setX(x)
                if self.isValidPosition(testPiece):
                    actions.append((r, testPiece.x))
        return actions

    def getTopLine(self, normalize=True):
        topLine = []
        for col in range(self.width):
            blockFound = False
            for row in range(self.height):
                if self.board[col][row] != BLANK:
                    topLine.append((row - 1, col))
                    blockFound = True
                    break
            if not blockFound:
                topLine.append((row, col))
        if normalize:
            return tuple(self.normalize(topLine))
        return topLine

    # normalize topLine adjust rows so that lowest rows become row (BOARDHEIGHT - 1), offset higher rows by this amount
    # columns are absolute. Do not adjust those.
    def normalize(self, topLine):
        highest = max(topLine, key=lambda i: i[0])[0]
        offset = self.height - 1 - highest
        if offset == 0:
            return topLine
        newTopLine = []
        for pair in topLine:
            newTopLine.append((pair[0] + offset, pair[1]))
        return newTopLine

    def isValidPosition(self, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        template = piece.getTemplate()
        for x in range(piece.width):
            for y in range(piece.height):
                isAboveBoard = y + piece.y + adjY < 0
                if isAboveBoard or template[y][x] == BLANK:
                    continue
                if not self.isOnBoard(x + piece.x + adjX, y + piece.y + adjY):
                    return False
                if self.board[x + piece.x + adjX][y + piece.y + adjY] != BLANK:
                    return False
        return True

    def isOnBoard(self, x, y):
        return x >= 0 and x < self.width and y < self.height

    def dropPiece(self, piece):
        # start piece at very top of board
        piece.setY(0)
        # drop piece in column
        i = 0
        while self.isValidPosition(piece, adjY=i):
            i += 1
        piece.setY(i - 1)

    def addToBoard(self, piece):
        self.dropPiece(piece)
        # fill in the board based on piece's location, shape, and rotation
        template = piece.getTemplate()
        for x in range(piece.width):
            for y in range(piece.height):
                if template[y][x] != BLANK:
                    self.board[x + piece.x][y + piece.y] = piece.color

    def isCompleteLine(self, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(self.width):
            if self.board[x][y] == BLANK:
                return False
        return True

    # edit game board and return number of lines removed
    def removeCompleteLines(self):
        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
        numLinesRemoved = 0
        y = self.height - 1 # start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(self.width):
                        self.board[x][pullDownY] = self.board[x][pullDownY-1]
                # Set very top line to blank.
                for x in range(self.width):
                    self.board[x][0] = BLANK
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1 # move on to check next row up
        return numLinesRemoved

    def getReward(self):
        """
        Get reward for changing state based on the rewards model we are testing/training.
        """
        numLinesRemoved = self.removeCompleteLines()

        # model 1
        # if numLinesRemoved == 0:
            # return -1
        # return numLinesRemoved * 1000

        # model 2
        return numLinesRemoved / float(1000)

        # model 3
        # if numLinesRemoved == 0:
            # return -0.001 / (self.width)
        # return numLinesRemoved / float(1000)
