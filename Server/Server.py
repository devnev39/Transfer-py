import socket
import threading
import ServerFileIo
import os

def setServerSpeedDelay(speed:int,delay:float):
    ServerFileIo.MAX_BYTES_PER_PACK = speed
    ServerFileIo.TRANSFER_DELAY_PER_PACK = delay

def setServerDirectoryRoot(root:str):
    if(os.path.isdir(root)):
        ServerFileIo.GLOBAL_SERVER_ROOT = root
    else:
        raise Exception("root path is not recognised !")

def setServerSocket(port:int):
    sck = socket.socket()
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sck.bind(("0.0.0.0",port))
    sck.listen(0)
    print(f'Server started with port {port}.')
    if(ServerFileIo.GLOBAL_SERVER_ROOT=="NONE"):
        raise Exception("First set serverDirectoryRoot by setServerDirectoryRoot() !")
    return sck

def acceptAndProcessSocket(sck:socket,func):
    try:    
        acc,addr = sck.accept()
        print(f'New connection from : {addr}')
        t = threading.Thread(target=func,args=(acc,))
        t.start()
    except Exception as exp:
        print(exp)
    