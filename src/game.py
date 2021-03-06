import pygame, sys, time
from config import *
from board import *
from pieceGenerator import *
from pygame.locals import *


class Game:
    def __init__(self, boardWidth, boardHeight):
        self.BOARDWIDTH = boardWidth
        self.BOARDHEIGHT = boardHeight
        self.XMARGIN = int((WINDOWWIDTH - self.BOARDWIDTH * BOXSIZE) / 2)
        self.TOPMARGIN = WINDOWHEIGHT - (self.BOARDHEIGHT * BOXSIZE) - 5

        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        pygame.display.set_caption('Tetroid')

        self.showTextScreen('Tetroid')

    def runGame(self, agent, autoplay=False):
        # setup variables for the start of the game
        board = Board(self.BOARDWIDTH, self.BOARDHEIGHT)
        generator = PieceGenerator()
        score = 0

        fallingPiece = generator.genRandPiece()
        nextPiece = generator.genRandPiece()

        nextState = agent.stateExtractor(board, fallingPiece, nextPiece)
        # get all actions for falling piece on board
        legalActions = board.getLegalActions(fallingPiece)
        if len(legalActions) == 0:
            return

        while True: # game loop
            # draw the current board
            if not autoplay:
                self.checkForQuit()
                # drawing everything on the screen
                self.DISPLAYSURF.fill(BGCOLOR)
                self.drawBoard(board.board)
                self.drawStatus(score)
                self.drawPiece(fallingPiece, pixelx=150, pixely=10)
                self.drawNextPiece(nextPiece)
                # while self.checkForKeyPress() == None:
                pygame.display.update()

            # update state
            state = nextState

            # choose action (using legalactions generated in the last iteration
            action = agent.getAction(state, legalActions)

            # take action
            fallingPiece.setAction(action)

            # add piece to the game board
            board.addToBoard(fallingPiece)

            # draw interim board if we are playing so we can see what's happening
            if not autoplay:
                self.drawBoard(board.board)
                # while self.checkForKeyPress() == None:
                pygame.display.update()

            # update board and get reward
            reward = board.getReward()
            score += reward

            # update state
            fallingPiece = nextPiece
            nextPiece = generator.genRandPiece()
            nextState = agent.stateExtractor(board, fallingPiece, nextPiece)

            # get legal actions for the new state
            legalActions = board.getLegalActions(fallingPiece)

            # if no more legal actions, game is over
            if len(legalActions) == 0:
                reward = -0.5
                agent.observeTransition(state, action, nextState, reward, legalActions)
                return

            # finally observe transition
            agent.observeTransition(state, action, nextState, reward, legalActions)

            if not autoplay:
                time.sleep(0.5)

    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForKeyPress(self):
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.
        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def showTextScreen(self, text):
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        self.DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.makeTextObjs('Press a key to play.', self.BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        self.DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        while self.checkForKeyPress() == None:
            pygame.display.update()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back

    def convertToPixelCoords(self, boxx, boxy):
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (self.XMARGIN + (boxx * BOXSIZE)), (self.TOPMARGIN + (boxy * BOXSIZE))

    def drawBox(self, boxx, boxy, color, pixelx=None, pixely=None):
        # draw a single box (each tetromino piece has four boxes)
        # at xy coordinates on the board. Or, if pixelx & pixely
        # are specified, draw to the pixel coordinates stored in
        # pixelx & pixely (this is used for the "Next" piece).
        if color == BLANK:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
        pygame.draw.rect(self.DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        pygame.draw.rect(self.DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

    def drawBoard(self, board):
        # draw the border around the board
        pygame.draw.rect(self.DISPLAYSURF, BORDERCOLOR, (self.XMARGIN - 3, self.TOPMARGIN - 7, (self.BOARDWIDTH * BOXSIZE) + 8, (self.BOARDHEIGHT * BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(self.DISPLAYSURF, BGCOLOR, (self.XMARGIN, self.TOPMARGIN, BOXSIZE * self.BOARDWIDTH, BOXSIZE * self.BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                self.drawBox(x, y, board[x][y])

    def drawStatus(self, score):
        # draw the score text
        scoreSurf = self.BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
        self.DISPLAYSURF.blit(scoreSurf, scoreRect)

    def drawPiece(self, piece, pixelx=None, pixely=None):
        shapeToDraw = piece.getTemplate()
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convertToPixelCoords(piece.x, piece.y)

        # draw each of the boxes that make up the piece
        for x in range(piece.width):
            for y in range(piece.height):
                if shapeToDraw[y][x] != BLANK:
                    self.drawBox(None, None, piece.color, pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

    def drawNextPiece(self, piece):
        # draw the "next" text
        nextSurf = self.BASICFONT.render('Next:', True, TEXTCOLOR)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOWWIDTH - 120, 80)
        self.DISPLAYSURF.blit(nextSurf, nextRect)
        # draw the "next" piece
        self.drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)
