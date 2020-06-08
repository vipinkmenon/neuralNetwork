import sys
import math
import os
from shutil import copyfile
from os import path

sourceFilePath = "./src/fpga/rtl/"
tbFilePath = "./src/fpga/tb/"

def writeIncludeFile(pretrained,numDenseLayers,dataWidth,layers,sigmoidSize,weightIntSize):
    # Create target Directory if don't exist
    if not os.path.exists(sourceFilePath):
        os.makedirs(sourceFilePath)
    if not os.path.exists(tbFilePath):
        os.makedirs(tbFilePath)
    f = open(sourceFilePath+"include.v","w")
    if pretrained == "Yes":
        f.write('`define pretrained\n')
    f.write("`define numLayers "+str(numDenseLayers)+'\n')
    f.write("`define dataWidth "+str(dataWidth)+'\n')
    i=1
    for i in range(1,len(layers)):
        f.write("`define numNeuronLayer%d %d\n"%(i,layers[i].getNumNeurons()))
        f.write("`define numWeightLayer%d %d\n"%(i,layers[i-1].getNumNeurons()))
        f.write('`define Layer%dActType "%s"\n'%(i,layers[i].getActivation()))
    f.write('`define sigmoidSize %d\n'%(sigmoidSize))
    f.write('`define weightIntWidth %d\n'%(weightIntSize))
    f.close()
    
    resources_dir = path.join(path.dirname(__file__), 'db/axi_lite_wrapper.v')
    copyfile(path.join(path.dirname(__file__), 'db/axi_lite_wrapper.v'), sourceFilePath+'axi_lite_wrapper.v')
    copyfile(path.join(path.dirname(__file__), 'db/neuron.v'), sourceFilePath+'neuron.v')
    copyfile(path.join(path.dirname(__file__), 'db/relu.v'), sourceFilePath+'relu.v')
    copyfile(path.join(path.dirname(__file__), 'db/Sig_ROM.v'), sourceFilePath+'Sig_ROM.v')
    copyfile(path.join(path.dirname(__file__), 'db/Weight_Memory.v'), sourceFilePath+'Weight_Memory.v')
    
def genLayer(layerNum,numNeurons,actType):
    fileName = sourceFilePath+"Layer_"+str(layerNum)+".v"
    f = open(fileName,"w")
    g = open(path.join(path.dirname(__file__),'db/layerInterface'))
    layerData = g.read()
    f.write('module Layer_%d #(parameter NN = 30,numWeight=784,dataWidth=16,layerNum=1,sigmoidSize=10,weightIntWidth=4,actType="relu")\n'%(layerNum))
    f.write(layerData)
    
    for i in range(numNeurons):
        f.write('\nneuron #(.numWeight(numWeight),.layerNo(layerNum),.neuronNo(%d),.dataWidth(dataWidth),.sigmoidSize(sigmoidSize),.weightIntWidth(weightIntWidth),.actType(actType),.weightFile("w_%d_%d.mif"),.biasFile("b_%d_%d.mif"))n_%d(\n\
        .clk(clk),\n\
        .rst(rst),\n\
        .myinput(x_in),\n\
        .weightValid(weightValid),\n\
        .biasValid(biasValid),\n\
        .weightValue(weightValue),\n\
        .biasValue(biasValue),\n\
        .config_layer_num(config_layer_num),\n\
        .config_neuron_num(config_neuron_num),\n\
        .myinputValid(x_valid),\n\
        .out(x_out[%d*dataWidth+:dataWidth]),\n\
        .outvalid(o_valid[%d])\n\
        );'%(i,layerNum,i,layerNum,i,i,i,i))
    f.write('\nendmodule')
    f.close()
    g.close()
    
    
def gentb():
    copyfile(path.join(path.dirname(__file__), 'db/top_sim.v'), tbFilePath+'top_sim.v')
    
def gen_nn(numLayers=0,layers=[],dataWidth=0,pretrained='Yes',weights=[],biases=[],sigmoidSize=10,weightIntSize=1,inputIntSize=4):
    #Sanity checks
    if numLayers != len(layers):
        print("Error:Number of specified layers does not match with the layers provided")
        sys.exit()
        
    
    if pretrained == 'Yes':
        i=0
        for layer in layers:
            if layer.type == "Dense" and layer.activation != "hardmax":
                try:
                    if layer.getNumNeurons() != len(weights[i]):
                        print("Number of weights do not match with number of neurons for layer {}".format(i))
                        sys.exit()
                    i += 1
                except:
                    print("Number of weights do not match with number of neurons")
            elif layer.type == "Dense":
                i += 1
    else:
        i=0
        for layer in layers:
            if layer.type == "Dense": 
                i += 1 
            
    writeIncludeFile(pretrained,i,dataWidth,layers,sigmoidSize,weightIntSize)     #Write the include file
        
    f = open(sourceFilePath+"zynet.v","w")
    g = open(path.join(path.dirname(__file__),"db/moduleTemplate"))
    data = g.read()
    g.close()
    f.write(data)
    
    
    f.write("""localparam IDLE = 'd0,
           SEND = 'd1;\n""") 
    #Instantiate the layers
    for i in range(1,numLayers):
        if layers[i].type == "Dense" and layers[i].activation != "hardmax":
            f.write("wire [`numNeuronLayer%d-1:0] o%d_valid;\n"%(i,i));
            f.write("wire [`numNeuronLayer%d*`dataWidth-1:0] x%d_out;\n"%(i,i));
            f.write("reg [`numNeuronLayer%d*`dataWidth-1:0] holdData_%d;\n"%(i,i))
            f.write("reg [`dataWidth-1:0] out_data_%d;\n"%(i))
            f.write("reg data_out_valid_%d;\n\n"%(i))
            genLayer(i,layers[i].getNumNeurons(),layers[i].getActivation)
            if i == 1: #First layer input is connected to AXI
                f.write("Layer_%d #(.NN(`numNeuronLayer%d),.numWeight(`numWeightLayer%d),.dataWidth(`dataWidth),.layerNum(%d),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer%dActType)) l%d(\n\t.clk(s_axi_aclk),\n\t.rst(reset),\n\t.weightValid(weightValid),\n\t.biasValid(biasValid),\n\t.weightValue(weightValue),\n\t.biasValue(biasValue),\n\t.config_layer_num(config_layer_num),\n\t.config_neuron_num(config_neuron_num),\n\t.x_valid(axis_in_data_valid),\n\t.x_in(axis_in_data),\n\t.o_valid(o%d_valid),\n\t.x_out(x%d_out)\n);\n\n"%(i,i,i,i,i,i,i,i))
            else: #All other layers
                f.write("Layer_%d #(.NN(`numNeuronLayer%d),.numWeight(`numWeightLayer%d),.dataWidth(`dataWidth),.layerNum(%d),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer%dActType)) l%d(\n\t.clk(s_axi_aclk),\n\t.rst(reset),\n\t.weightValid(weightValid),\n\t.biasValid(biasValid),\n\t.weightValue(weightValue),\n\t.biasValue(biasValue),\n\t.config_layer_num(config_layer_num),\n\t.config_neuron_num(config_neuron_num),\n\t.x_valid(data_out_valid_%d),\n\t.x_in(out_data_%d),\n\t.o_valid(o%d_valid),\n\t.x_out(x%d_out)\n);\n\n"%(i,i,i,i,i,i,i-1,i-1,i,i))
            if layers[i].activation != "hardmax":
                f.write("//State machine for data pipelining\n\n")
                f.write("reg       state_%d;\n"%(i))
                f.write("integer   count_%d;\n"%(i))
                f.write("always @(posedge s_axi_aclk)\n")
                f.write("begin\n\
    if(reset)\n\
    begin\n\
        state_%d <= IDLE;\n\
        count_%d <= 0;\n\
        data_out_valid_%d <=0;\n\
    end\n\
    else\n\
    begin\n\
        case(state_%d)\n\
            IDLE: begin\n\
                count_%d <= 0;\n\
                data_out_valid_%d <=0;\n\
                if (o%d_valid[0] == 1'b1)\n\
                begin\n\
                    holdData_%d <= x%d_out;\n\
                    state_%d <= SEND;\n\
                end\n\
            end\n\
            SEND: begin\n\
                out_data_%d <= holdData_%d[`dataWidth-1:0];\n\
                holdData_%d <= holdData_%d>>`dataWidth;\n\
                count_%d <= count_%d +1;\n\
                data_out_valid_%d <= 1;\n\
                if (count_%d == `numNeuronLayer%d)\n\
                begin\n\
                    state_%d <= IDLE;\n\
                    data_out_valid_%d <= 0;\n\
                end\n\
            end\n\
        endcase\n\
    end\n\
end\n\n"%(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i))
        elif layers[i].activation == "hardmax":
            copyfile(path.join(path.dirname(__file__),'db/maxFinder.v'), sourceFilePath+'maxFinder.v')
            f.write("reg [`numNeuronLayer%d*`dataWidth-1:0] holdData_%d;\n"%(i-1,i)) 
            f.write("assign axi_rd_data = holdData_%d[`dataWidth-1:0];\n\n"%(i))
            f.write("always @(posedge s_axi_aclk)\n\
    begin\n\
        if (o%d_valid[0] == 1'b1)\n\
            holdData_%d <= x%d_out;\n\
        else if(axi_rd_en)\n\
        begin\n\
            holdData_%d <= holdData_%d>>`dataWidth;\n\
        end\n\
    end\n\n\n"%(i-1,i,i-1,i,i))
    
            f.write("maxFinder #(.numInput(`numNeuronLayer%d),.inputWidth(`dataWidth))\n\
    mFind(\n\
        .i_clk(s_axi_aclk),\n\
        .i_data(x%d_out),\n\
        .i_valid(o%d_valid),\n\
        .o_data(out),\n\
        .o_data_valid(out_valid)\n\
    );\n"%(i-1,i-1,i-1))
    
    
    
    f.write("endmodule")
    
    
    f.close()
    
    
    gentb()
    
    
    f = open(sourceFilePath+"sigContent.mif","w")
        
    fractBits = sigmoidSize-(weightIntSize+inputIntSize) 
    if fractBits < 0: #Sigmoid size is smaller the integer part of the MAC operation
        fractBits = 0
    #Generating Sigmoid LUT content
    x = -2**(weightIntSize+inputIntSize-1)#Smallest input going to the Sigmoid LUT from the neuron
    for i in range(0,2**sigmoidSize):
        y = sigmoid(x)
        z = DtoB(y,dataWidth,dataWidth-inputIntSize)
        f.write(z+'\n')
        x=x+(2**-fractBits)
        
    f.close()

def DtoB(num,dataWidth,fracBits):#funtion for converting into two's complement format
    if num >= 0:
        num = num * (2**fracBits)
        num = int(num)
        e = bin(num)[2:]
    else:
        num = -num
        num = num * (2**fracBits)#number of fractional bits
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = 2**dataWidth - num
        e = bin(d)[2:]
    return e
    
    
def sigmoid(x):
    try:
        return 1 / (1+math.exp(-x))
    except:
        return 0