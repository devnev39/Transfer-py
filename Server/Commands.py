import time
from Server import ServerFileIo

GLOBAL_COMMAND_PARAMS = {
    "ls" : 0,
    "cd" : 1,
    "get" : 1
}

def executeServerLSCmd(cmd,acc):
    acc.send(ServerFileIo.getCurrentFolderListing().encode())

def executeServerCDCmd(cmd,acc):
    try:
        ServerFileIo.changeCurrentServerRoot(cmd.split(" ")[1])
        acc.send(ServerFileIo.getCurrentFolderListing().encode())
    except Exception as ex:
        print(ex)
        acc.send(str(ex).encode())

def executeServerGetCmd(cmd,acc):
    req = cmd.split(" ")[-1]
    try:
        if(not ServerFileIo.checkRequest(req)):
            acc.send(str(0).encode())
            raise Exception(ServerFileIo.bcolors.WARNING+'file/folder not found !'+ServerFileIo.bcolors.ENDC)
        acc.send(str(1).encode())
        if(ServerFileIo.isDirectory(req)):
            acc.send(ServerFileIo.getRequestFolderContent(req).encode())
            conf = int(acc.recv(50))
            if(conf):
                pass
            else:
                raise Exception(ServerFileIo.bcolors.FAIL+"Transfer cancelled !"+ServerFileIo.bcolors.ENDC)
            pass
        if(ServerFileIo.isFile(req)):
            acc.send(ServerFileIo.getRequestFileProperties(req).encode())
            conf = int(acc.recv(512))
            if(conf):
                ServerFileIo.sendFile(req,acc)
            else:
                raise Exception(ServerFileIo.bcolors.FAIL+"Transfer cancelled !"+ServerFileIo.bcolors.ENDC)
    except Exception as exp:
        print(exp)
        time.sleep(0.1)
        acc.send(str(exp).encode())

GLOBAL_SERVER_COMMAND_BINDER = {
    "ls" : executeServerLSCmd,
    "cd" : executeServerCDCmd,
    "get" : executeServerGetCmd
}

def executeServerCommandQuery(cmd:str,acc):
    split = cmd.split(" ")
    if(GLOBAL_COMMAND_PARAMS.get(split[0]) > len(split[1:])):
        acc.send("Command parameter not found !")
        print("Command parameter not received !")
        return 
    
    GLOBAL_SERVER_COMMAND_BINDER.get(split[0])(cmd,acc)
