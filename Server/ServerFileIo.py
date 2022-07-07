import math
import os
from socket import socket
import time

GLOBAL_SERVER_ROOT = "NONE"

MAX_BYTES_PER_PACK = 40960
TRANSFER_DELAY_PER_PACK = 0.005

LAST_FOLDER_FILES = []

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

def checkRequest(req:str):
    if(not os.path.exists(os.path.join(GLOBAL_SERVER_ROOT,req))):
        return 0
    return 1

def isDirectory(req):
    if(os.path.isdir(os.path.join(GLOBAL_SERVER_ROOT,req))):
        return 1
    return 0

def isFile(req):
    if(os.path.isfile(os.path.join(GLOBAL_SERVER_ROOT,req))):
        # print(req)
        return 1
    return 0

def getSize(req):
    return os.path.getsize(os.path.join(GLOBAL_SERVER_ROOT,req))

def getRequestFileProperties(req):
    size = getSize(req)
    LAST_FOLDER_FILES.append(os.path.join(GLOBAL_SERVER_ROOT,req))
    return f'Name : {req}\nSize : {size}'

def getRequestFolderContent(req,f_c,s_c):
    n_f,n_s = 0,0
    if(isFile(req)):
        LAST_FOLDER_FILES.append(req)
        return f_c+1,s_c+getSize(req)
    if(isDirectory(req)):
        for each in os.listdir(os.path.join(GLOBAL_SERVER_ROOT,req)):
            a,b = getRequestFolderContent(os.path.join(GLOBAL_SERVER_ROOT,req,each),n_f,n_s)
            n_f = a
            n_s = b
    return n_f+f_c,n_s+s_c

def resetFileFolderNameCache():
    LAST_FOLDER_FILES.clear()

def processFileFolderRequest(req,acc):
    files_no = len(LAST_FOLDER_FILES)
    acc.send(str(files_no).encode())
    time.sleep(0.1)
    for file_ind in range(files_no):
        s = os.path.getsize(LAST_FOLDER_FILES[file_ind])
        acc.send(str(s).encode())
        time.sleep(0.1)
        acc.send(str(MAX_BYTES_PER_PACK).encode())
        time.sleep(0.1)
        sendFile(LAST_FOLDER_FILES[file_ind],s,acc)

def sendFile(name:str,size,acc:socket):
    packs = math.ceil(size/MAX_BYTES_PER_PACK)
    short_name = name.split(GLOBAL_SERVER_ROOT+os.path.sep)[-1]
    acc.send(short_name.encode())
    time.sleep(0.1)
    with(open(name,"rb")) as f:
        if packs==1 : 
            acc.send(f.read(size))
            print(f'SENT : {name}')
            return
        sent = 0
        for pack in range(1,packs+1):
            if(pack==packs):
                read_size = size - (1024*(pack-1))
                sent += read_size
                acc.send(f.read(read_size))
                print(f'Done : {(sent/size)*100}',end="\r")
                continue
            acc.send(f.read(MAX_BYTES_PER_PACK))
            time.sleep(TRANSFER_DELAY_PER_PACK)
            sent += MAX_BYTES_PER_PACK
            print(f'Done : {(sent/size)*100} %',end='\r')