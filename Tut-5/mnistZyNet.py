from zynet import zynet
from zynet import utils
import numpy as np

def genMnistZynet(dataWidth,sigmoidSize,weightIntSize,inputIntSize):
    model = zynet.model()
    model.add(zynet.layer("flatten",784))
    model.add(zynet.layer("Dense",30,"relu"))
    model.add(zynet.layer("Dense",30,"relu"))
    model.add(zynet.layer("Dense",10,"relu"))
    model.add(zynet.layer("Dense",10,"relu"))
    model.add(zynet.layer("Dense",10,"hardmax"))
    weightArray = utils.genWeightArray('WeigntsAndBiasesReLuNew.txt')
    biasArray = utils.genBiasArray('WeigntsAndBiasesReLuNew.txt')
    model.compile(pretrained='Yes',weights=weightArray,biases=biasArray,dataWidth=dataWidth,weightIntSize=weightIntSize,inputIntSize=inputIntSize,sigmoidSize=sigmoidSize)
    #zynet.makeXilinxProject('myProject1','xc7z020clg484-1')
    #zynet.makeIP('myProject1')
    #zynet.makeSystem('myProject1','myBlock2')
    
if __name__ == "__main__":
    genMnistZynet(dataWidth=16,sigmoidSize=5,weightIntSize=4,inputIntSize=1)