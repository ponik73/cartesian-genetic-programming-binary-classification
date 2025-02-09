import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from fixedPoint import fixedPointBinary

DATASET_PATH = 'data/original/data_banknote_authentication.txt'
NUM_CLASSES = 2

def __loadDataset():
    data = pd.read_csv(DATASET_PATH, sep=",", header=None)
    data.columns = ["variance", "skewness", "kurtosis", "entropy", "class"]
    return data

if __name__ == "__main__":

    df = __loadDataset()

    df, representation = fixedPointBinary(df)

    trainDf, testDf = train_test_split(df, test_size=int(np.round(df.shape[0]*0.1)), random_state=123)

    binaryOutput = lambda x: "0" * (NUM_CLASSES - x) + "1" + "0" * (abs(1 - x))

    trainDf["class"] = trainDf["class"].apply(lambda x: x + 1)
    trainDf["class"] = trainDf["class"].apply(binaryOutput)

    testDf["class"] = testDf["class"].apply(lambda x: x + 1)
    testDf["class"] = testDf["class"].apply(binaryOutput)

    with open('data/fixedpoint/banknote.txt', "w") as f:
        for index, row in trainDf.iterrows():
            f.write(f'{row["variance"]} {row["skewness"]} {row["kurtosis"]} {row["entropy"]} : {row["class"]}\n')

    testDf.to_csv('data/fixedpoint/banknoteTest.txt', index=False, header=False, sep=" ")
    # with open(f'banknoteTest.txt', "w") as f:
    #     for index, row in testDf.iterrows():
    #         f.write(f'{row["variance"]} {row["skewness"]} {row["kurtosis"]} {row["entropy"]} : {row["class"]}\n')