# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, copy, pickle
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 5
BOARDHEIGHT = 8
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

# offsets given as (x_left, x_right, y_top)
OFFSETS = {'S': [(1, 1, 2), (2, 1, 1)],
          'Z': [(1, 1, 2), (1, 2, 1)],
          'I': [(2, 2 ,0), (0, 1, 2)],
          'O': [(1, 2, 2)],
          'J': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)],
          'L': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)],
          'T': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)]}

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT

    args = readCommand( sys.argv[1:] ) # Set game options for agent based on input
    agent = args['agent']
    willExport = args['export']
    valuesLoaded = args['valuesLoaded']

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetroid')

    if not valuesLoaded:
        while agent.isInTraining():
            agent.startEpisode()
            runGame(agent, inTesting=False)
            if agent.shouldStopEpisode():
                agent.stopEpisode()
                averageRewards = agent.episodeRewards / agent.gamesInEpisode
                print "TESTING GAMES UP TO " + str(agent.gamesInEpisode * agent.episodesSoFar)
                print "Average Rewards for this set of episodes: " + str(averageRewards)
                showTextScreen("Game Over")
            agent.recordGame()
            print agent.gamesSoFar

        if willExport:
            writeToFile(agent.q_values)

    # now we are testing
    while True:
        runGame(agent)
        showTextScreen("Game Over")


def runGame(agent, inTesting=True):
    # setup variables for the start of the game
    board = getBlankBoard()
    score = 0

    fallingPiece = None
    nextPiece = getNewPiece()
    observeTransition = False

    while True: # game loop
        if fallingPiece != None:
            prevState = (topLine, fallingPiece['shape'], nextPiece['shape'])
            prevAction = (rotation, column)
            observeTransition = True

        # get falling piece
        fallingPiece = nextPiece
        nextPiece = getNewPiece()

        # get all actions for falling piece on board
        legalActions = getLegalActions(board, fallingPiece)
        if len(legalActions) == 0:
            return

        topLine = getTopLine(board)

        # observe state change
        state = (topLine, fallingPiece['shape'], nextPiece['shape'])
        if observeTransition:
            agent.observeTransition(prevState, prevAction, state, reward, legalActions)

        # choose random action
        rotation, column = agent.getAction(state, legalActions)

        # set piece options based on action
        fallingPiece['rotation'] = rotation
        fallingPiece['x'] = column
        fallingPiece['y'] = 0 - OFFSETS[fallingPiece['shape']][rotation][2]

        # drop piece in column
        i = 0
        while isValidPosition(board, fallingPiece, adjY=i):
            i += 1
        fallingPiece['y'] += i - 1

        addToBoard(board, fallingPiece)

        # draw interim board if in testing so we can see what's happening
        if inTesting:
            drawBoard(board)
            while checkForKeyPress() == None:
                pygame.display.update()

        # reward function
        reward = getReward(board)
        score += reward

        checkForQuit()
        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score)
        drawNextPiece(nextPiece)

        if inTesting:
            while checkForKeyPress() == None:
                pygame.display.update()


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': 0,
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def getTopLine(board):
    topLine = []
    for col in range(BOARDWIDTH):
        blockFound = False
        for row in range(BOARDHEIGHT):
            if board[col][row] != BLANK:
                topLine.append((row - 1, col))
                blockFound = True
                break
        if not blockFound:
            topLine.append((row, col))
    # normalize topLine adjust rows so that lowest rows become row 0 (19), offset higher rows by this amount
    # columns are absolute. Do not adjust those.
    return tuple(normalize(topLine))

def normalize(topLine):
    highest = max(topLine, key=lambda i: i[0])[0]
    offset = BOARDHEIGHT - 1 - highest
    if offset == 0:
        return topLine
    newTopLine = []
    for pair in topLine:
        newTopLine.append((pair[0] + offset, pair[1]))
    return newTopLine

def getLegalActions(board, piece):
    actions = []
    for rotation in range(len(PIECES[piece['shape']])):
        xLOffset, xROffset, yOffset = OFFSETS[piece['shape']][rotation]
        testPiece = copy.deepcopy(piece)
        testPiece['rotation'] = rotation
        testPiece['y'] = 0 - yOffset
        for x in range(0 - xLOffset, BOARDWIDTH):
            testPiece['x'] = x
            if not isValidPosition(board, testPiece):
                continue
            actions.append((rotation, testPiece['x']))
    return actions


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved

def getReward(board):
    numLinesRemoved = removeCompleteLines(board)
    if numLinesRemoved == 0:
        return -1
    return 1000 * numLinesRemoved

def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


def writeToFile(d):
    with open("values.txt", "wb") as f:
        pickle.dump(d, f)

# NEEDS IMPLEMENTATION
def readDictFile(file):
    with open(file, "rb") as f:
        d=pickle.load(f)
    return d


def parseAgentArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts


def readCommand(argv):
    from optparse import OptionParser

    # THIS USAGE STRING IS STILL IN PROGRESS AND SHOULD BE DISREGARDED UNTIL COMPLETION
    usageStr = """
    USAGE:      python tetris.py <options>
    EXAMPLES:   (1) python tetroid.py
                    - use the Random Agent
                (2) python tetroid.py --agent QLearningAgent --agentArgs numTraining=5
                OR python tetroid.py -t QLearningAgent -a numTraining=5
                    - begins training tetroid agent with 5 sets of training episodes
    """

    parser = OptionParser(usageStr)

    parser.add_option('-t', '--agent', dest='agent',
                      help='the agent TYPE to use', default='RandomAgent')
    parser.add_option('-a','--agentArgs',dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--export', dest='exportValues',
                      action='store_true', default=False, help='Export Learned q-values/weights for future testing')
    parser.add_option('-l', '--load', dest='dictFile',
                      help='Read in a dictionary from FILE', metavar='FILE')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    agentOpts = parseAgentArgs(options.agentArgs)
    tetroidType = loadAgent(options.agent)

    if options.dictFile:
        values = readDictFile(options.dictFile)
        valuesLoaded = True
        tetroid = tetroidType(values=values)
    else:
        valuesLoaded = False
        tetroid = tetroidType(**agentOpts)

    args = dict()
    args['agent'] = tetroid
    args['export'] = options.exportValues
    args['valuesLoaded'] = valuesLoaded
    return args


def loadAgent(tetroid):
    module = __import__("agents")
    return getattr(module, tetroid)


if __name__ == '__main__':
    main()
