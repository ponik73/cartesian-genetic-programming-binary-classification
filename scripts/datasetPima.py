import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from fixedPoint import fixedPointBinary

DATASET_PATH = 'data/original/pima-indians-diabetes.txt'
NUM_CLASSES = 2

def __loadDataset():
    data = pd.read_csv(DATASET_PATH, sep=",", header=None)
    data = data.rename(columns={8: "class"})
    return data

if __name__ == "__main__":
    df = __loadDataset()

    df, representation = fixedPointBinary(df)
    
    trainDf, testDf = train_test_split(df, test_size=int(np.round(df.shape[0]*0.1)), random_state=123)
    
    binaryOutput = lambda x: "01" if x == 0 else "10"
    
    trainDf["class"] = trainDf["class"].apply(binaryOutput)

    testDf["class"] = testDf["class"].apply(binaryOutput)

    with open('data/fixedpoint/pima.txt', "w") as f:
        for index, row in trainDf.iterrows():
            f.write(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]} : {row["class"]}\n')

    testDf.to_csv('data/fixedpoint/pimaTest.txt', index=False, header=False, sep=" ")


