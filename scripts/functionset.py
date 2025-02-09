import numpy as np

functionsPy = {
    "const": "lambda x, _: 1",#const
    "in1": "lambda x, _: x", #identity
    # "not in1": "lambda x, _: np.bitwise_not(x).astype(int)", #inversion
    # "or": "lambda x, y: np.bitwise_or(x,y).astype(int)", # Bitwise OR
    # "orNeg1": "lambda x, y: np.bitwise_or(np.bitwise_not(x).astype(int),y).astype(int)", # Bitwise ~i1 OR i2
    # "and": "lambda x, y: np.bitwise_and(x,y).astype(int)", # Bitwise AND
    # "nand": "lambda x, y: np.bitwise_not(np.bitwise_and(x,y)).astype(int)", # Bitwise NAND
    # "xor": "lambda x, y: np.bitwise_xor(x,y).astype(int)", # Bitwise XOR
    # "rshift1": "lambda x, _: np.right_shift(x,1)", # Right shift by 1
    # "rshift2": "lambda x, _: np.right_shift(x,2)", # Right shift by 2
    # "add": "lambda x, y: x + y", # Addition
    # "addSat": "lambda x, y: min(max(x + y, 0), 255)", # Addition with saturation
    # "avg": "lambda x, y: np.right_shift(x,1) + np.right_shift(y,1)",
    # "max": "lambda x, y: max(x,y)", # Maximum
    # "min": "lambda x, y: min(x,y)", # Minimum
    # Logical:
    "not in1": "lambda x, _: np.logical_not(x).astype(int)", #inversion
    "or": "lambda x, y: np.logical_or(x,y).astype(int)", # Bitwise OR
    "orNeg1": "lambda x, y: np.logical_or(np.logical_not(x).astype(int),y).astype(int)", # Bitwise ~i1 OR i2
    "and": "lambda x, y: np.logical_and(x,y).astype(int)", # Bitwise AND
    "nand": "lambda x, y: np.logical_not(np.logical_and(x,y)).astype(int)", # Bitwise NAND
    "xor": "lambda x, y: np.logical_xor(x,y).astype(int)", # Bitwise XOR
    "nor": "lambda x, y: np.logical_not(np.logical_or(x,y)).astype(int)",
    "xnor": "lambda x, y: np.logical_not(np.logical_xor(x,y)).astype(int)",
    "avg": "lambda x, y: np.right_shift(x,1) + np.right_shift(y,1)",
    "max": "lambda x, y: max(x,y)", # Maximum
    "min": "lambda x, y: min(x,y)", # Minimum
}

functionsC = {
    "const": "*pnodeout++ = 255;",
    "in1": "*pnodeout++ = in1;",
    "not in1": "*pnodeout++ = ~in1;",
    "or": "*pnodeout++ = in1 | in2;",
    "orNeg1": "*pnodeout++ = (~in1) | in2;", # Bitwise ~i1 OR i2
    "and": "*pnodeout++ = in1 & in2;",
    "nand": "*pnodeout++ = ~(in1 & in2);",
    "xor": "*pnodeout++ = in1 ^ in2;",
    "rshift1": "*pnodeout++ = in1 >> 1;", # Right shift by 1
    "rshift2": "*pnodeout++ = in1 >> 2;", # Right shift by 2
    "add": "*pnodeout++ = in1 + in2;", # Addition
    "addSat": "*pnodeout++ = ((((in1 + in2) > 0) ? (in1 + in2) : 0) > 255) ? 255 : (((in1 + in2) > 0) ? (in1 + in2) : 0);", # Addition with saturation
    "avg": "*pnodeout++ = (in1 >> 1) + (in2 >> 1);",
    "max": "*pnodeout++ = (in1 > in2) ? in1 : in2;", # Maximum
    "min": "*pnodeout++ = (in1 > in2) ? in2 : in1;", # Minimum


    "nor": "*pnodeout++ = ~(in1 | in2);",
    "xnor": "*pnodeout++ = ~(in1 ^ in2);"
}

def __generatePy(func):
    return functionsPy[func]

def __generateC(func):
    return functionsC[func]

def generateFunctionsets():
    py = {}
    c = {}
    for i, f in enumerate(FUNCTION_SET):
        py[i] = f'{__generatePy(f)},'
        c[f'case {i}'] = f'{__generateC(f)} break;'
    return py, c

FUNCTION_SET = ['const', 'in1', 'not in1', 'or', 'orNeg1', 'and', 'nand', 'xor']
# FUNCTION_SET = [
#     "const",
#     "in1",
#     "not in1",
#     "or",
#     "orNeg1",
#     "and",
#     "nand",
#     "xor",
#     # "rshift1",
#     # "rshift2",
#     # "add",
#     # "addSat",
#     "avg",
#     "max",
#     "min"
#     # "xnor"
# ]

def printFunctionSet(fset):
    for key, value in fset.items():
        print(f'{str(key)}: {str(value)}')

    

if __name__ == "__main__":
    setPy, setC = generateFunctionsets()
    print(f'Functions: {FUNCTION_SET}')
    print()
    printFunctionSet(setPy)
    print()
    printFunctionSet(setC)
    print("default: abort();")