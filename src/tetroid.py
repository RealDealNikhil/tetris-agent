"""
Tetroid
By Nikhil Suri and Soumil Singh

Adapted from:
Tetronimo (a tetris clone)
By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pygame
Released under a "Simplified BSD" license
"""

import cPickle
from game import *

def main():

    args = readCommand( sys.argv[1:] ) # Set game options for agent based on input
    agent = args['agent']
    exportFile = args['exportFile']
    train = args['train']
    test = args['test']
    progressTracker = args['progress']
    play = args['play']
    boardWidth, boardHeight = map(lambda i: int(i), args['board'])

    game = Game(boardWidth, boardHeight)

    trainingInfo = None
    testingInfo = None

    # train agent.
    if train:
        trainingInfo = runEpisodes(game, agent, progressTracker, True)

        if exportFile:
            writeToFile(exportFile, agent.getValues())

        agent.endTraining()

    # test agent
    if test:
        testingInfo = runEpisodes(game, agent, progressTracker, False)

    printList(trainingInfo)
    printList(testingInfo)

    if play:
        game.runGame(agent)
        game.showTextScreen("Game Over")

    # FOR EXTRACTING POLICY
    # if play:
        # i = 0
        # while i < 1000:
            # game.runGame(agent, autoplay=True)
            # if i % 1000 == 0:
                # print game.weights
            # # game.showTextScreen("Game Over")
            # i += 1
        # print game.weights
        # writeToFile("extractedWeights", game.weights)

    print agent.getValues()

def runEpisodes(game, agent, progressTracker, inTraining):
    episodesInfo = []
    agent.startEpisode()
    if inTraining:
        check = agent.isInTraining
        infoString = "TRAINING"
    else:
        check = agent.isInTesting
        infoString = "TESTING"
    while check():
        game.runGame(agent, autoplay=True)
        # game.runGame(agent)
        agent.recordGame()
        if agent.gamesSoFar % progressTracker == 0:
            print agent.gamesSoFar
            print agent.getValues()
        if agent.shouldStopEpisode():
            agent.stopEpisode()
            averageRewards = agent.episodeRewards / agent.gamesPerEpisode
            gameSet = str(agent.gamesSoFar - agent.gamesPerEpisode) + "-" + str(agent.gamesSoFar)
            episodesInfo.append(
                infoString + " GAMES " + gameSet + "\t\t" +
                "Average Rewards for this set of episodes: " + str(averageRewards))
            agent.startEpisode()
    return episodesInfo

def printList(l):
    try:
        for el in l:
            print el
    except TypeError:
        pass

def writeToFile(fileName, d):
    filePath = "../values/" + fileName + ".pickle"
    with open(filePath, "wb") as f:
        cPickle.dump(d, f)

def readDictFile(fileName):
    filePath = "../values/" + fileName + ".pickle"
    with open(filePath, "rb") as f:
        d = cPickle.load(f)
    return d

def parseAgentArgs(args, willTrain):
    opts = {}

    if args is not None:
        pieces = args.split(',')
        for p in pieces:
            if '=' in p:
                key, val = p.split('=')
            else:
                key,val = p, 1
            opts[key] = val

    if not willTrain:
        opts['epsilon'] = 0.0
        opts['alpha'] = 0.0

    return opts

def readCommand(argv):
    from optparse import OptionParser

    # THIS USAGE STRING IS STILL IN PROGRESS AND SHOULD BE DISREGARDED UNTIL COMPLETION
    usageStr = """
    USAGE:      python tetris.py <options>
    EXAMPLES:   (1) python tetroid.py
                    - use the Random Agent
                (2) python tetroid.py --agent QLearningAgent --agentArgs numTraining=5
                OR python tetroid.py -a QLearningAgent -g numTraining=5
                    - begins training tetroid agent with 5 sets of training episodes
    """

    parser = OptionParser(usageStr)

    parser.add_option('-a', '--agent', dest='agent',
                      help='the agent TYPE to use', default='RandomAgent')
    parser.add_option('-g','--agentArgs',dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--export', dest='exportFile',
                      help='Export Learned q-values/weights to ../values/FILENAME for future testing. Do not include filename extension',
                      metavar='FILENAME')
    parser.add_option('-l', '--load', dest='dictFile',
                      help='Read in a dictionary from ../values/FILENAME. Do not include filename extension',
                      metavar='FILENAME')
    parser.add_option('--test', dest='test',
                      action='store_true', default=False,
                      help='Test agent')
    parser.add_option('--train', dest='train',
                      action='store_true', default=False,
                      help='Train agent from scratch or using loaded values')
    parser.add_option('-p', '--progress', dest='progressTracker', default=1, type='int',
                      help='Set the rate at which we show the completion of games')
    parser.add_option('-n', '--no-play', dest='play',
                      action='store_false', default=True,
                      help='DO NOT play game')
    parser.add_option('-b', '--board', dest='board_dim',
                      default='10x20', help='Set board dimensions. Given as WIDTHxHEIGHT')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    agentOpts = parseAgentArgs(options.agentArgs, options.train)
    tetroidType = loadAgent(options.agent)

    if options.dictFile:
        values = readDictFile(options.dictFile)
        tetroid = tetroidType(values=values, **agentOpts)
    else:
        tetroid = tetroidType(**agentOpts)

    board_dim = options.board_dim.split('x')
    if len(board_dim) != 2:
        raise Exception('Invalid board dimensions. Dimensions should be given as WIDTHxHEIGHT')

    args = {
        'agent': tetroid,
        'exportFile': options.exportFile,
        'test': options.test,
        'train': options.train,
        'progress': options.progressTracker,
        'play': options.play,
        'board': board_dim
    }
    return args

def loadAgent(tetroid):
    module = __import__("agents")
    return getattr(module, tetroid)

if __name__ == '__main__':
    main()
