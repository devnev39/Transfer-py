import os
GLOBAL_SERVER_ROOT = "NONE"

def getCurrentFolderListing():
    if(not os.path.isdir(GLOBAL_SERVER_ROOT)):
        raise Exception("valid GLOBAL_SERVER_ROOT not set !")
    res = ""
    for ele in os.listdir(GLOBAL_SERVER_ROOT):
        res += "\n"+ele
    return res

def changeCurrentServerRoot(newRoot:str):
    global GLOBAL_SERVER_ROOT
    if(not os.path.isdir(os.path.join(GLOBAL_SERVER_ROOT,newRoot))):
        raise Exception("valid dir not formed !")
    GLOBAL_SERVER_ROOT = os.path.join(GLOBAL_SERVER_ROOT,newRoot)

