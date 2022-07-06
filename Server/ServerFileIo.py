import os
GLOBAL_SERVER_ROOT = "NONE"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getCurrentFolderListing():
    if(not os.path.isdir(GLOBAL_SERVER_ROOT)):
        raise Exception("valid GLOBAL_SERVER_ROOT not set !")
    res = "======"+bcolors.OKGREEN+GLOBAL_SERVER_ROOT+bcolors.ENDC+"======"
    for ele in os.listdir(GLOBAL_SERVER_ROOT):
        if(os.path.isdir(os.path.join(GLOBAL_SERVER_ROOT,ele))):
            res += "\n"+bcolors.HEADER+ele+"->"+bcolors.ENDC
        else:    
            res += "\n"+ele
    return res+bcolors.ENDC+"\n\t======\n"

def changeCurrentServerRoot(newRoot:str):
    global GLOBAL_SERVER_ROOT
    if(newRoot==".."):
        GLOBAL_SERVER_ROOT = str(os.path.sep).join(GLOBAL_SERVER_ROOT.split(os.path.sep)[:-1])
        return
    if(not os.path.isdir(os.path.join(GLOBAL_SERVER_ROOT,newRoot))):
        raise Exception("valid dir not formed !")
    GLOBAL_SERVER_ROOT = os.path.join(GLOBAL_SERVER_ROOT,newRoot)

