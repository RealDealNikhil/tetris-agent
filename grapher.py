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
