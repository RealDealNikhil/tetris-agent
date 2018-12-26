# Experiments

We conducted many experiments which consisted of multiple training and testing episodes. We recorded the results of every single experiment we ran, and stored the learned Q-values and weights (for exact and approximate learning, respectively) using [cPickle](https://docs.python.org/2/library/pickle.html#module-cPickle). Below is an overview of all the pickle files in our repository, including their naming schema and a description of what tests they each represent.

Note that we only saved records of training the approximate agent on rewards model 2. This was done for a couple of reasons. First, the results for the approximate agent on model 1 were terrible - the agent learned to maximize features it was expected to minimize - so we saw no reason to keep files of learned weights for model 1. Second, the results for the approximate agent on model 3 were similar to those on model 2. However, the approximate agent performed better on average under model 3. Since the training time for the approximate agent is quite short, we decided to not store these learned weights (for model 3) either.

The general process for experimentation was the following:
1. Train the agent for some number of iterations (games).
2. Test the agent using those learned values for some number of games.
3. Repeat steps 1. and 2. to build upon these learned values.

The first set of files store values that were learned after training on rewards model 1. This rewards model gives a reward of +1000 for every line clear and -1 otherwise. There is no penalty given for losing the game. These files all contain values learned by an exact q learning agent on a 5x8 board, tested over 10K iterations for every 50K training iterations. Testing results are recorded below each.
* **#KIters:** Files with names such as 50KIters and 100KIters. Trained with decreasing alpha and epsilon (both start at 0.5 and decrease by 0.01 every 50K iterations).
    * 50K: 3974.3119
    * 100K: 3369.0422
    * 150K: 2775.8194
    * 200K: 2378.5158
    * 250K: 2341.3141
    * 300K: 2103.9978
    * 350K: 2086.5395
    * 400K: 1961.1225
    * 450K: 1978.6635
    * 500K: 1885.2355

* **#KLow:** Files with names such as 50KLow and 100KLow. Trained with 0.05 alpha and 0.5 epsilon.
    * 50K: 4184.6715
    * 100K: 5314.6428
    * 150K: 5985.7316
    * 200K: 6440.5043
    * 250K: 6622.5076
    * 300K: 6799.0901
    * 350K: 6919.0074
    * 400K: 6824.0173
    * 450K: 6794.7143
    * 500K: 6820.9814

* **#KLowFork:** Files with names such as 50KLowFork and 100KLowFork. Same training as #KLow files until 400K iterations, where alpha was reduced to 0.01 and epsilon reduced to 0.1.
    * 400K: 6936.2825
    * 450K: 6979.6623
    * 500K: 6950.4985

* **#KLow2:** Files with names such as 50KLow2 and 100KLow2. Trained with 0.01 alpha and 0.2 epsilon.
    * 50K: 4693.1441
    * 100K: 5916.6021
    * 150K: 6525.0343
    * 200K: 6959.3481
    * 250K: 7158.061
    * 300K: 7324.7742
    * 350K: 7419.8426
    * 400K: 7540.1846
    * 450K: 7637.9374
    * 500K: 7686.6417

The second set of files store values that were learned after training on rewards model 2. This rewards model gives a reward of +0.001 for every line clear and -0.5 for losing the game. There is no living penalty that is enacted if the agent picks an action that does not clear any lines.
* **#KNew:** Files with names such as 50KNew and 100KNew. Exact learning agent trained on a 5x8 board with 0.05 alpha and 0.5 epsilon. Average rewards taken over 10K testing games.
    * 50K: 2.6834
    * 100K: 2.881
    * 150K: 3.025
    * 200K: 2.986
    * 250K: 2.987
    * 300K: 2.982

* **#KNewLow:** Files with names such as 50KNewLow and 100KNewLow. Exact learning agent trained on a 5x8 board with 0.01 alpha and slowly decreasing epsilon (start at 0.5, decrease by 0.05 every 50K iterations). Average rewards taken over 10K testing games.
    * 50K: 2.82
    * 100K: 3.06
    * 150K: 3.14
    * 200K: 3.27
    * 250K: 3.28
    * 300K: 3.3
    * 350K: 3.31
    * 400K: 3.32

* **#KNewLowFork:** Files with names such as 50KNewLowFork. Same training as #KNewLow files until 400K iterations, where epsilon was set back to 0.5.
    * 400K: 3.37
    * 450K: 3.37

* **#KM2:** Files with names such as 50KM2 and 100KM2. Exact learning agent trained on a 5x8 board with 0.01 alpha and 0.2 epsilon. Average rewards taken over 10K testing games.
    * 50K: 2.91
    * 100K: 3.1
    * 150K: 3.15
    * 200K: 3.25
    * 250K: 3.29
    * 300K: 3.36
    * 350K: 3.42
    * 400K: 3.47
    * 450K: 3.41
    * 500K: 3.43

* **#M2Comp:** Files with names such as 500M2Comp and 1000M2Comp. Exact learning agent trained on a 5x8 board for 500 iterations at a time with 0.01 alpha and 0.2 epsilon. Average rewards taken over 500 testing games.
    * 500: 0.07
    * 1000: 0.1
    * 1500: 0.08
    * 2000: 0.12
    * 2500: 0.06
    * 3000: 0.09

* **#KNew6x8:** Files with names such as 50KNew6x8 and 100KNew6x8. Exact learning agent trained on a 6x8 board with 0.01 alpha and 0.5 epsilon. Average rewards taken over 10K testing games.
    * 50K: 1.47
    * 100K: 1.74
    * 150K: 1.89
    * 200K: 2
    * 250K: 2.1
    * 300K: 2.18
    * 350K: 2.24
    * 400K: 2.33
    * 450K: 2.38

* **#KNew5x10:** Files with names such as 50KNew5x10. Exact learning agent trained on a 5x10 board with 0.01 alpha and 0.5 epsilon. Average rewards taken over 10K testing games.
    * 50K: 3.23
    * 100K: 3.55
    * 150K: 3.77
    * 200K: 3.88
    * 250K: 4
    * 300K: 4
    * 350K: 4.03
    * 400K: 4.1
    * 450K: 4.11
    * 500K: 4.15

* **300TrainFeatures:** Weights for approximate learning agent trained on a 10x20 board with 0.05 alpha and 0.2 epsilon for 300 iterations. Used numHoles, bias, avgHeightDiff, highestPoint features. Average rewards over 20 testing games of **136.2**.

* **300TrainFeatures2:** Weights for approximate learning agent trained on a 10x20 board with 0.05 alpha and 0.5 epsilon for 300 iterations. Used numHoles, bias, avgHeightDiff, highestPoint features. Average rewards over 20 testing games of **147.25**.

* **#TrainFeatures3:** Files are 300TrainFeatures3 and 600TrainFeatures 3. Weights for approximate learning agent trained on a 10x20 board with 0.05 alpha and 0.5 epsilon for 300 iterations at a time. Used numHoles, bias, avgHeightDiff, aggregateHeight features. Average rewards taken over 20 testing games.
    * 300: 339.35
    * 600: 351.75 

* **#FM2:** Files with names such as 500FM2 and 1000FM2. Approximate learning agent trained on a 5x8 board with 0.01 alpha and 0.2 epsilon for 500 iterations at a time. Used aggregateHeight, numHoles, avgHeightDiff, bias features. Average rewards taken over 20 testing games.
    * 500: 20.81
    * 1000: 19.64
    * 1500: 17.88
    * 2000: 16.0
    * 2500: 22.31
    * 3000: 20.21

The next few sets of files compare different combinations of heuristics for the approximate learning agent against each other. Training was done under rewards model 2 on a 10x20 board with 0.01 alpha and 0.5 epsilon for 300 iterations at a time. Average rewards were taken over 20 testing games.
* **#TestFeatures1:** Files with names such as 300TestFeatures1. Used numHoles, highestPoint, bias, avgHeightDiff features.
    * 300: 163.7
    * 600: 176.05
    * 900: 171.9

* **#TestFeatures2:** Files with names such as 300TestFeatures2. Used squaredHoleSize, highestPoint, bias, avgHeightDiff features.
    * 300: 8.6
    * 600: 10.55
    * 900: 9.15

* **#TestFeatures3:** Files with names such as 300TestFeatures3. Used numHoles, aggregateHeight, bias, avgHeightDiff features.
    * 300: 390.05
    * 600: 428.2
    * 900: 359.9

* **#TestFeatures4:** Files with names such as 300TestFeatures4. Used squaredHoleSize, aggregateHeight, bias, avgHeightDiff features.
    * 300: 368.5
    * 600: 588.95
    * 900: 432.4

The third set of files store values that were learned after training on rewards model 3. This rewards model gives a reward of +0.001 for every line clear and -0.5 for losing the game. There is also a living penalty of -0.001/*b*, where *b* is the width of the board. These files all contain values learned by an exact learning agent over training set of 50K games on a 5x8 board. Average rewards were all taken over 10K testing games.
* **#KM3:** 0.05 alpha and 0.5 epsilon.
    * 50K: 1.27
    * 100K: 1.58
    * 150K: 1.65
    * 200K: 1.64
    * 250K: 1.69
    * 300K: 1.65
    * 350K: 1.63

* **#KM3Low:** 0.01 alpha and 0.2 epsilon. Results for this set were all very similar.
    * 50K: 0.012
    * 100K: 0.012
    * 150K: 0.012
    * 200K: 0.012
    * 250K: 0.012
    * 300K: 0.012
    * 350K: 0.012
    * 400K: 0.012
