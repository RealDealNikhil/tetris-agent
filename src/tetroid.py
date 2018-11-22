# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pickle
from game import *

def main():

    args = readCommand( sys.argv[1:] ) # Set game options for agent based on input
    agent = args['agent']
    willExport = args['export']
    valuesLoaded = args['valuesLoaded']

    game = Game()

    # we have not loaded any pre-set values. We must train agent.
    if not valuesLoaded:
        while agent.isInTraining():
            agent.startEpisode()
            game.runGame(agent, inTesting=False)
            if agent.shouldStopEpisode():
                agent.stopEpisode()
                averageRewards = agent.episodeRewards / agent.gamesInEpisode
                print "TESTING GAMES UP TO " + str(agent.gamesInEpisode * agent.episodesSoFar)
                print "Average Rewards for this set of episodes: " + str(averageRewards)
                game.showTextScreen("Game Over")
            agent.recordGame()
            print agent.gamesSoFar

        if willExport:
            writeToFile(agent.q_values)

    # now we are testing
    while True:
        game.runGame(agent)
        game.showTextScreen("Game Over")



def writeToFile(d):
    with open("values.txt", "wb") as f:
        pickle.dump(d, f)


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
