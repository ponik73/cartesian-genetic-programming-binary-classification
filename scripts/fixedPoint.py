import pandas as pd
import numpy as np

def fixedPointBinary(df: pd.DataFrame, precision=0.001):
    decimalSpaces = int(abs(np.log10(precision)))
    bits = lambda x: int(np.ceil(np.log2(x)))
    
    highestInt = int(np.round(df.max().max())) << 3
    bitsCountInt = bits(highestInt) # INT (8 BIT);

    highestDecimal = int(np.round(((1 - precision)/precision), decimals=decimalSpaces))
    bitsCountDecimal = bits(highestDecimal) # DECIMAL (10 BIT)

    representation = {
        "signBit": 1,
        "intBits": bitsCountInt,
        "decimalBits": bitsCountDecimal
    }
    
    signBit = lambda x: "1" if x < 0 else "0"
    intBits = lambda x: np.binary_repr(abs(int(x)), width=bitsCountInt)
    def decimal(x):
        x = abs(x)
        x = np.round(np.modf(x)[0], decimals=decimalSpaces)
        x = x / precision
        x = int(np.round(x))
        if x > highestDecimal:
            return highestDecimal
        return x
    
    decimalBits = lambda x: np.binary_repr(decimal(x), width=bitsCountDecimal)
    
    dfFixedPoint = pd.DataFrame({"placeholder": np.zeros(len(df.iloc[:, 0]))})
    
    for seriesName, series in df.items():
        if seriesName == "class":
            dfFixedPoint[seriesName] = series
            continue

        fp = pd.DataFrame({"signBit": series.apply(signBit)})
        fp["intBits"] = series.apply(intBits)
        fp["decimalBits"] = series.apply(decimalBits)
        fp["fpRepr"] = fp["signBit"] + fp["intBits"] + fp["decimalBits"]
        dfFixedPoint[seriesName] = fp["fpRepr"]

    dfFixedPoint = dfFixedPoint.drop(columns=["placeholder"], axis=0)

    return dfFixedPoint, representation

# TODO function that turns fixed point binary representation back to decimal
# def fixedPointDecimal(df, representation):