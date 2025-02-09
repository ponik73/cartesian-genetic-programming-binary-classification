import pandas as pd
from sklearn.model_selection import train_test_split
from fixedPoint import fixedPointBinary

DATASET_PATH = 'data/original/data_banknote_authentication.txt'
NUM_CLASSES = 2

def __loadDataset():
    data = pd.read_csv('winequality-white.csv', sep=";", header=0)
    return data

if __name__ == "__main__":

    df = __loadDataset()

    df, representation = fixedPointBinary(df)

    #TODO
    # NUM_CLASSES = 
    # trainDf, testDf = train_test_split(df, test_size=10, random_state=123)
    # binaryOutput = lambda x: "0" * (NUM_CLASSES - x) + "1" + "0" * (abs(1 - x))

    # with open('wine.txt', "w") as f:
    #     for index, row in trainDf.iterrows():
    #         f.write(f'{row["fixed acidity"]} {row["volatile acidity"]} {row["citric acid"]} {row["residual sugar"]} {row["chlorides"]} {row["free sulfur dioxide"]} {row["total sulfur dioxide"]} {row["density"]} {row["pH"]} {row["sulphates"]} {row["alcohol"]} : {row["quality"]}\n')

    # with open('wineTest.txt', "w") as f:
    #     for index, row in testDf.iterrows():
    #         f.write(f'{row["fixed acidity"]} {row["volatile acidity"]} {row["citric acid"]} {row["residual sugar"]} {row["chlorides"]} {row["free sulfur dioxide"]} {row["total sulfur dioxide"]} {row["density"]} {row["pH"]} {row["sulphates"]} {row["alcohol"]} : {row["quality"]}\n')
