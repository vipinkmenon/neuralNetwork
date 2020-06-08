from os import system
from os import path

def makeVivadoProject(projectName='myProject',fpgaPart="xc7z020clg484-1"):
    system("Vivado -mode tcl -source "+path.join(path.dirname(__file__),'db/vivadoScript.tcl')+" -tclargs "+fpgaPart)
    f=open("zynet.tcl","a")
    f.write("\nset_property source_mgmt_mode All [current_project]")
    f.write("\nexit") #Vivado doesn't add exit command to the end of the script
    f.close()
    system("Vivado -mode tcl -source zynet.tcl -tclargs --project_name "+projectName)
    
def makeIP(projectName='myProject'):
    system("Vivado -mode tcl -source "+path.join(path.dirname(__file__),'db/makeIP.tcl')+" -tclargs "+projectName)
    
def makeSystem(projectName='myProject',ipPath="",blockName=""):
    system("Vivado -mode tcl -source "+path.join(path.dirname(__file__),'db/block.tcl')+" -tclargs "+projectName+" "+ipPath+" "+blockName)