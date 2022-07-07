import math
from socket import socket
import os

GLOBAL_RECEIVING_DIRECTORY = os.path.join(os.getcwd(),"Received")

def executeLSClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

def executeCDClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

def createDirectory(name):
    if(not os.path.exists(GLOBAL_RECEIVING_DIRECTORY)):
        os.mkdir(GLOBAL_RECEIVING_DIRECTORY)
    split = name.split(os.path.sep)[:-1]
    prev = ""
    for each in split:
        if(not os.path.exists(os.path.join(GLOBAL_RECEIVING_DIRECTORY,prev,each))):
            os.mkdir(os.path.join(GLOBAL_RECEIVING_DIRECTORY,prev,each))
        if(prev==""):
            prev = each
            continue
        prev = os.path.join(prev,each)

def executeGetClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    res = int(sck.recv(50))
    if(res):
        print(sck.recv(1024).decode())
        conf = int(input("Confirm (0 to decline otherwise 1) : "))
        sck.send(str(conf).encode())
        if(not conf):
            print(sck.recv(1024).decode())
        else:
            file_no = int(sck.recv(512))
            for file in range(1,file_no+1):
                size = int(sck.recv(512))
                pack_len = int(sck.recv(512))
                name = sck.recv(1024).decode()
                print(name)
                createDirectory(name)
                with(open(os.path.join(GLOBAL_RECEIVING_DIRECTORY,name),"wb")) as f:
                    packs = math.ceil(size/pack_len)
                    if packs == 1:
                        f.write(sck.recv(size))
                        f.close()
                        print(f'Received : {f.name}',end='\r')
                    current_len = 0
                    for pack in range(1,packs+1):
                        if(pack==packs):
                            remain_read = size-(pack_len*(pack-1))
                            f.write(sck.recv(remain_read))
                            current_len += remain_read
                            print(f'Done : {round((current_len/size)*100,2)} %',end='\r')
                            continue
                        f.write(sck.recv(pack_len))
                        current_len += pack_len
                        print(f'Done : {round((current_len/size)*100,2)} %',end='\r')
                    f.close()
    else:
        print(sck.recv(1024).decode())

CLIENT_COMMAND_PROCEDURE_BINDER = {
    "ls" : executeLSClientCmd,
    "cd" : executeCDClientCmd,
    "get" : executeGetClientCmd,
}

def checkCommand(cmd:str):
    if(not list(CLIENT_COMMAND_PROCEDURE_BINDER.keys()).count(cmd.split(" ")[0])):
        return 0
    return 1

def executeCommand(cmd:str,sck:socket):
    target = CLIENT_COMMAND_PROCEDURE_BINDER.get(cmd.split(" ")[0])
    target(cmd,sck)