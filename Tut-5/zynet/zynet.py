from zynet import gen_nn
from zynet import genWegitsAndBias
import os
from zynet import xilinxUtils

class layer:
    def __init__(self,type="flatten",numNeurons=0,activation=""):
        self.type = type
        self.numNeurons = numNeurons
        if type == "Dense":
            self.activation = activation
    def getNumNeurons(self):
        return self.numNeurons
    def getActivation(self):
        return self.activation
        
class model:
    def __init__(self):
        self.numLayers = 0
        self.layers = []
    def add(self,layer):
        self.numLayers += 1
        self.layers.append(layer)
    def getNumLayers(self):
        return self.numLayers
    def compile(self,pretrained='No',weights="",biases="",dataWidth=16,sigmoidSize=5,weightIntSize=1,inputIntSize=4):
        gen_nn.gen_nn(self.numLayers,self.layers,dataWidth,pretrained=pretrained,weights=weights,biases=biases,sigmoidSize=sigmoidSize,weightIntSize=weightIntSize,inputIntSize=inputIntSize)
        if pretrained=='Yes':
            genWegitsAndBias.genWegitsAndBias(dataWidth,dataWidth-weightIntSize,dataWidth-weightIntSize-inputIntSize,weights,biases)
    
def makeXilinxProject(projectName='myProject',fpgaPart='xc7z020clg484-1'):
    xilinxUtils.makeVivadoProject(projectName,fpgaPart)
    
def makeIP(projectName):
    xilinxUtils.makeIP(projectName+'/'+projectName+'.xpr')
    
def makeSystem(projectName,blockName):
    xilinxUtils.makeSystem(projectName+'/'+projectName+'.xpr',projectName+'/../src/',blockName)