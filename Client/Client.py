import Connector
import Commands
import sys

sck = Connector.ConnectToFirst(8899)
print(sck.recv(1024).decode())
while(1):
    inp = input("Enter cmd : ")
    try:
        if(not Commands.checkCommand(inp)):
            print("Enter a valid command !")
            continue
        Commands.executeCommand(inp,sck)
    except Exception as exp:
        a,b,exc_tb = sys.exc_info()
        print(exp)
        print(exc_tb.tb_lineno)
        break