# Experiments

We conducted many experiments which consisted of multiple training and testing episodes. We recorded the results of every single experiment we ran, and stored the learned Q-values and weights (for exact and approximate learning, respectively) using [cPickle](https://docs.python.org/2/library/pickle.html#module-cPickle). Below is an overview of all the pickle files in our repository, including their naming schema and a description of what tests they each represent.

Note that we only saved records of training the approximate agent on rewards model 2. This was done for a couple of reasons. First, the results for the approximate agent on model 1 were terrible - the agent learned to maximize features it was expected to minimize - so we saw no reason to keep files of learned weights for model 1. Second, the results for the approximate agent on model 3 were similar to those on model 2. However, the approximate agent performed better on average under model 3. Since the training time for the approximate agent is quite short, we decided to not store these learned weights (for model 3) either.

The first set of files store values that were learned after training on rewards model 1. This rewards model gives a reward of +1000 for every line clear and -1 otherwise. There is no penalty given for losing the game.
* **#KIters**

* **#KLow**

* **#KLowFork**

* **#KLow2**

The second set of files store values that were learned after training on rewards model 2. This rewards model gives a reward of +0.001 for every line clear and -0.5 for losing the game. There is no living penalty that is enacted if the agent picks an action that does not clear any lines.
* **#KNew**

* **#KNewLow**

* **#KNewLowFork**

* **#KM2**

* **M2Comp**

* **#KNew6x8**

* **#KNew5x10**

* **300TrainFeatures**

* **300TrainFeatures2**

* **300TrainFeatures3**

* **600TrainFeatures3**

* **#FM2**

* **#TestFeatures1**

* **#TestFeatures2**

* **#TestFeatures3**

* **#TestFeatures4**

The third set of files store values that were learned after training on rewards model 3. This rewards model gives a reward of +0.001 for every line clear and -0.5 for losing the game. There is also a living penalty of -0.001/*b*, where *b* is the width of the board.

* **#KM3**

* **#KM3Low**
