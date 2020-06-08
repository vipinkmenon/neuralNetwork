import json
import math

def genWeightArray(fileName=""):
    output = []
    weightFile = open(fileName,"r")
    myData = weightFile.read()
    myDict = json.loads(myData)
    myWeights = myDict['weights']
    #print(max(myWeights))
    reemovNestings(myWeights,output)
    maxVal = max(output)
    minVal = min(output)
    minBits = max(math.ceil(math.log2(abs(int(maxVal))+1)),math.ceil(math.log2(abs(int(minVal))+1)))+1 #One additional bit for sign
    print("Minimum bits required for integer representation of Weight Values",minBits)
    return myWeights
    
    
def genBiasArray(fileName=""):
	biasFile = open(fileName,"r")
	myData = biasFile.read()
	myDict = json.loads(myData)
	myBiases = myDict['biases']
	return myBiases
    
    
def reemovNestings(l,output): #Recursive function to flatten a multi-dimensional list
    for i in l: 
        if type(i) == list: 
            reemovNestings(i,output) 
        else: 
            output.append(i) 