import Connector
import Commands

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
        print(exp)
        break

        
