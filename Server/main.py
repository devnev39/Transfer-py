import Server
import Process
import sys

try:
    if(len(sys.argv) == 2):
        Server.setServerSpeedDelay(sys.argv[0],sys.argv[1])
    else:
        Server.setServerSpeedDelay(40960,0.005)
    root = input("Enter valid root : ")
    Server.setServerDirectoryRoot(root)
    sck = Server.setServerSocket(8899)
    while(1):
        Server.acceptAndProcessSocket(sck,Process.processSocket)
except Exception as ex:
    print(ex)