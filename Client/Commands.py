from socket import socket

def executeLSClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

def executeCDClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

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
            pass
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