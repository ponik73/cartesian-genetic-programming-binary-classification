import re
import numpy as np
import pandas as pd

class Node:
    def __init__(self, nodeId, function, in1Id, in2Id):
        self.id = nodeId
        self.function = function
        self.in1Id = in1Id
        self.in2Id = in2Id
        self.value = None
    def setValue(self, value):
        self.value = value
    def evaluate(self, in1, in2):
        self.value = self.function(in1, in2)#.astype(int)
        # print(self.function, in1, in2, self.value)

class Grid:
    def __init__(self, functionSet):
        self.functionSet = functionSet
        self.nodes: list[Node] = []
        self.inputIds = []
    def addNode(self, node):
        self.nodes.append(node)
    def __getNodeById(self, nodeId):
        for x in self.nodes:
            if x.id == nodeId:
                return x
        return None
    def __updateNodeValue(self, nodeId, value):
        for x in self.nodes:
            if x.id != nodeId:
                continue
            x.value = value
    def __setInputs(self, idsAndVals):
        for nodeId, val in idsAndVals:
            self.__updateNodeValue(nodeId, val)
            self.inputIds.append(nodeId)
    def evalChromosome(self, idsAndVals, outputIds):
        self.__setInputs(idsAndVals)

        for n in self.nodes:
            if n.id in self.inputIds:
                continue
            in1 = self.__getNodeById(n.in1Id)
            in2 = self.__getNodeById(n.in2Id)
            if in1 is None:
                print(n.in1Id)
            n.evaluate(in1.value, in2.value)

        res = []
        for i in outputIds:
            res.append(self.__getNodeById(i))
        return res
    
    def __evalNode(self, nodeId):
        node = self.__getNodeById(nodeId)

        in1 = self.__getNodeById(node.in1Id)
        if in1.id not in self.inputIds:
            self.__evalNode(in1.id)

        in2 = self.__getNodeById(node.in1Id)    
        if in2.id not in self.inputIds:
            self.__evalNode(in2.id)
            
        node.evaluate(in1.value, in2.value)

    def clearNodes(self):
        for n in self.nodes:
            n.setValue(None)

def getTestValues():
    df = pd.read_csv(TEST_DATA_PATH, sep=" ", header=None, dtype=str)
    inputSeries = df.iloc[:, :-1].apply(lambda row: ''.join(row.astype(str)), axis=1)
    classSeries = df.iloc[:, -1].astype(str)
    df = pd.DataFrame({
        "input": inputSeries,
        "class": classSeries,
        "predictedClass": ""
    })
    return df

def parseChromosome(grid: Grid, inputIds: list[int], chromosome: str):
    for i in inputIds:
        grid.addNode(Node(i, None, None, None))

    def extractFromBlock(block):
        match = re.search(r"\[(\d+)\](\d+)(.*)", block)
        if match:
            other_numbers = [int(match.group(2))]
            other_numbers.extend([int(num) for num in re.findall(r"\d+", match.group(3))])
            return int(match.group(1)), other_numbers[0], other_numbers[1], other_numbers[2]
        else:
            print(block)

    blocks = re.findall(r"\([^)]+\)", chromosome)
    for b in blocks:
        nodeId, in1Id, in2Id, function = extractFromBlock(b)
        grid.addNode(Node(nodeId, grid.functionSet[function], in1Id, in2Id))


TEST_DATA_PATH_BANKNOTE = "data/fixedpoint/banknoteTest.txt"
TEST_DATA_PATH_PIMA = "data/fixedpoint/pimaTest.txt"
INPUT_IDS_BANKNOTE = list(range(0,76))
INPUT_IDS_PIMA = list(range(0,192))

TEST_DATA_PATH = TEST_DATA_PATH_PIMA
INPUT_IDS = INPUT_IDS_PIMA

if __name__ == "__main__":
    chromosome = "([192]30,128,5)([193]167,102,3)([194]109,130,3)([195]143,170,0)([196]100,138,5)([197]61,59,5)([198]176,193,5)([199]194,83,5)([200]192,196,7)([201]195,100,7)([202]199,60,7)([203]39,41,4)([204]198,160,4)([205]201,157,7)([206]200,197,4)([207]108,61,6)([208]134,53,4)([209]114,191,3)([210]206,204,6)([211]205,202,6)([212]210,211,6)([213]9,209,3)([214]145,19,6)([215]162,3,5)([216]69,145,5)"
    outputIds = [210,212]
    inputIds = INPUT_IDS

    functionSet = {
0: lambda x, _: 1,
1: lambda x, _: x,
2: lambda x, _: np.logical_not(x).astype(int),
3: lambda x, y: np.logical_or(x,y).astype(int),
4: lambda x, y: np.logical_or(np.logical_not(x).astype(int),y).astype(int),
5: lambda x, y: np.logical_and(x,y).astype(int),
6: lambda x, y: np.logical_not(np.logical_and(x,y)).astype(int),
7: lambda x, y: np.logical_xor(x,y).astype(int),
    }
    fpRepreToList = lambda x: [int(digit) for digit in str(x)]


    grid = Grid(functionSet)
    parseChromosome(grid, inputIds, chromosome)


    testDf = getTestValues()

    for index, row in testDf.iterrows():
        inputValues = fpRepreToList(row["input"])
        res = grid.evalChromosome(list(zip(inputIds, inputValues)), outputIds)
        res = [x.value for x in res]
        # res = [0 if x == 0 else 1 for x in res] ###
        row["predictedClass"] = ''.join([str(x) for x in res])
        grid.clearNodes()

    testDf["correctPrediction"] = testDf["class"] == testDf["predictedClass"]

    countCorrect = testDf["correctPrediction"].value_counts()[True]
    countIncorrect = testDf["correctPrediction"].value_counts()[False]
    classifierAccuracy = countCorrect / (countCorrect + countIncorrect)
    classifierAccuracy = np.round(classifierAccuracy * 100, decimals=2)

    print("True: ", countCorrect)
    print("False: ", countIncorrect)
    print("Accuracy: ", classifierAccuracy)
    
    