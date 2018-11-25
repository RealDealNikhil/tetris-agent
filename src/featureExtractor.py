import util

class Extractor:
    def getFeatures(self, state, action):
        features = util.Counter()
        # features will be
        # 1. number of lines we will clear by taking the action
        # 2. difference between height of adjacent columns on the board
        # 3. highest point in board
        # 4. total holes in board
        # since state also includes the next piece, we may be able to take this a step further
        # to do this, we will
        # 1. addToBoard(board, fallingpiece) - this edits the board directly
        # 2. removeCompleteLines(board) - this returns the number of lines that we remove
        # 3. we will now have an edited board, so we can easily calculate the bumpiness, highest point, total holes
