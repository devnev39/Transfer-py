import Commands

def processSocket(acc):
    test = "Commands : \n1.ls\n2.cd\n3.get"
    acc.send(test.encode())
    while(1):
        cmd = acc.recv(256).decode()
        Commands.executeServerCommandQuery(cmd,acc)