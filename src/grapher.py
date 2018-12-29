import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

values = {
    "alpha=0.5, epsilon=0.5": [
        3974.3119,
        3369.0422,
        2775.8194,
        2378.5198,
        2341.3141,
        2103.9978,
        2086.5395,
        1961.1225,
        1978.6635,
        1885.2355
    ],
    "alpha=0.05, epsilon=0.5": [
        4184.6715,
        5314.6428,
        5985.7316,
        6440.5043,
        6622.5076,
        6799.0901,
        6919.0074,
        6824.0173,
        6794.7143,
        6820.9814
    ],
    "alpha=0.01, epsilon=0.1 (from 400K onwards)": [
        4184.6715,
        5314.6428,
        5985.7316,
        6440.5043,
        6622.5076,
        6799.0901,
        6919.0074,
        6936.2825,
        6979.6623,
        6950.4985
    ]
}

index = ['50K', '100K', '150K', '200K', '250K', '300K', '350K', '400K', '450K', '500K']

df = pd.DataFrame(values, index)

lines = df.plot.line()
plt.xticks(np.arange(len(df)), df.index)
plt.show()


values = {
    "alpha=0.01, epsilon=0.5 (5x8 board)": [
        2.82270000028,
        3.05780000031,
        3.14360000031,
        3.26540000033,
        3.28290000033,
        3.30220000033,
        3.31080000033,
        3.31510000032,
        3.36660000033
        
    ],
    
    "alpha=0.01, epsilon=0.5 (6x8 board)": [
        1.46580000016,
        1.73990000018,
        1.8916000002,
        2.00030000021,
        2.09850000022,
        2.18040000023,
        2.24330000024,
        2.32760000024,
        2.37710000025
        
    ],
    "alpha=0.01, epsilon=0.5 (5x10 board)": [
        3.22950000032,
        3.54950000036,
        3.77210000038,
        3.87920000039,
        3.9962000004,
        3.9896000004,
        4.0333000004,
        4.09700000041,
        4.11460000041
        
    ],
    
       
}

index = ['50K', '100K', '150K', '200K', '250K', '300K', '350K', '400K', '450K']
    
df = pd.DataFrame(values, index)

lines = df.plot.line()
plt.xticks(np.arange(len(df)), df.index)
plt.ylabel("avg number of lines cleared")
plt.xlabel("number of training game iterations")
plt.title('Performance of exact Q-learning model on different boards')
plt.savefig('boardsize.png')
plt.show()

#old vs new exact Q-learning model

values = {
    "alpha=0.01, epsilon=0.2 (Model 1)": [
        4.6931441,
        5.9166021,
        6.5250343,
        6.9593481,
        7.158061,
        7.3247742,
        7.4198426,
        7.5401846,
        7.6379374,
        7.6866417
    ],
    "alpha=0.01, epsilon=0.2 (Model 2)": [
        2.90790000029,
        3.07410000031,
        3.15170000031,
        3.24580000032,
        3.29360000032,
        3.35900000033,
        3.42090000033,
        3.46670000034,
        3.41280000033,
        3.43430000033
    ],
    "alpha=0.01, epsilon=0.2 (Model 3)": [
        1.2117,
        1.28719,
        1.44784,
        1.53288,
        1.69118,
        1.68584,
        1.76158,
        1.82798,
        1.84671,
        1.88811
    ],
          
         }

index = ['50K', '100K', '150K', '200K', '250K', '300K', '350K', '400K', '450K', '500k']
    
df = pd.DataFrame(values, index)

lines = df.plot.line()
plt.xticks(np.arange(len(df)), df.index)
plt.ylabel("avg number of lines cleared")
plt.xlabel("number of training game iterations")
plt.title('Performance of exact Q-learning models 1, 2 and 3')
plt.savefig('exactmodels123.png')
plt.show()

#heuristic testing graph


values = {
    "Feature Set 1": [
        163.7,
        176.05,
        171.9,
    ],
    "Feature Set 2": [
        8.6,
        10.55,
        9.15,
    ],
    "Feature Set 3": [
        390.05,
        428.2,
        359.9,
    ],
    "Feature Set 4": [
        368.5,
        588.95,
        432.4,
    ],
          
         }

index = ['300', '600', '900']
    
df = pd.DataFrame(values, index)

lines = df.plot.line()
plt.xticks(np.arange(len(df)), df.index)
plt.ylabel("avg number of lines cleared")
plt.xlabel("number of training game iterations")
plt.title("Performance of Approximate Q Agent With Different Features")
plt.savefig('heuristics.png')
plt.show()

#approx vs exact Q-learning on 5x8 board a = 0.01 and e = 0.2

values = {
    "alpha=0.01, epsilon=0.2 Approximate Model": [
        20.81,
        19.64,
        17.88,
        16.0,
        22.31,
        20.21,
    ],
    "alpha=0.01, epsilon=0.2 Exact Model": [
        0.0699999999999,
        0.0999999999999,
        0.0800000000001,
        0.12,
        0.06,
        0.0899999999999,
    ],
          
         }

index = ['500', '1000', '1500', '2000', '2500', '3000']
    
df = pd.DataFrame(values, index)

lines = df.plot.line()
plt.xticks(np.arange(len(df)), df.index)
plt.ylabel("avg number of lines cleared")
plt.xlabel("number of training game iterations")
plt.title('Approximate vs. Exact Q-learning Model')
plt.savefig("exactvsapprox.png")
plt.show()

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


#approxModel2 = [104.0, 493.0, 82.0, 788.0, 47.0, 133.0, 439.0, 194.0, 166.0, 194.0, 124.0, 571.0, 981.0, 123.0, 281.0, 173.0, 262.0, 351.0, 592.0, 689.0]
approxModel2 = [415.0, 198.0, 381.0, 897.0, 43.0, 193.0, 647.0, 11.0, 760.0, 122.0, 42.0, 948.0, 522.0, 563.0, 9.0, 57.0, 192.0, 541.0, 140.0, 354.0]
approxModel3 = [223, 504, 45, 539, 197, 357, 138, 37, 424, 15, 859, 650, 77, 1214, 259, 230, 154, 105, 74, 507]

count1 = 0
for i in approxModel2:
    count1 += i
print(count1/len(approxModel2))


count2 = 0
for i in approxModel3:
    count2 += i
print(count2/len(approxModel3))

objects = ('Approx Model 2', 'Approx Model 3')
y_pos = np.arange(len(objects))
performance = [351.75,330.4]


plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('avg number of lines cleared')
plt.title('Approx Model 2 vs. Model 3 Performance')
plt.savefig('approxmodel23.png')
plt.show()


