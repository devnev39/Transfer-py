# import os
import Server
import Process

try:
    root = input("Enter valid root : ")
    Server.setServerDirectoryRoot(root)
    sck = Server.setServerSocket(8899)
    while(1):
        Server.acceptAndProcessSocket(sck,Process.processSocket)
except Exception as ex:
    print(ex)