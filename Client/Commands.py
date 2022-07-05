from socket import socket

def executeLSClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

def executeCDClientCmd(cmd:str,sck:socket):
    sck.send(cmd.encode())
    print(sck.recv(1024).decode())

def executeGetClientCmd(cmd,sck):
    pass

CLIENT_COMMAND_PROCEDURE_BINDER = {
    "ls" : executeLSClientCmd,
    "cd" : executeCDClientCmd,
    "get" : executeGetClientCmd,
}

def checkCommand(cmd:str):
    if(not list(CLIENT_COMMAND_PROCEDURE_BINDER.keys()).count(cmd.split(" ")[0])):
        return 0
    return 1

def executeCommand(cmd:str,sck):
    target = CLIENT_COMMAND_PROCEDURE_BINDER.get(cmd.split(" ")[0])
    target(cmd,sck)