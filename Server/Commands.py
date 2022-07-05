from Server import ServerFileIo

GLOBAL_COMMAND_PARAMS = {
    "ls" : 0,
    "cd" : 1,
    "get" : 1
}

def executeServerLSCmd(cmd,acc):
    acc.send(ServerFileIo.getCurrentFolderListing().encode())
    pass

def executeServerCDCmd(cmd,acc):
    try:
        ServerFileIo.changeCurrentServerRoot(cmd.split(" ")[1])
        acc.send(ServerFileIo.getCurrentFolderListing().encode())
    except Exception as ex:
        print(ex)
        acc.send(str(ex).encode())

def executeServerGetCmd(cmd,acc):
    pass

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
