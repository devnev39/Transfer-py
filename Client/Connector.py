import socket

def ConnectToFirst(port:int):
    sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sck.connect(("8.8.8.8",80))
    ip = ".".join(str(sck.getsockname()[0]).split(".")[:3])
    for i in range(0,256):
        new_ip = ip+"."+str(i)
        try:
            sck_t = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sck_t.settimeout(0.2)
            sck_t.connect((new_ip,port))
            print(f'Connected to {new_ip} on port {port}')
            sck_t.settimeout(None)
            return sck_t
        except Exception as exp:
            print(f'Unreachable : {new_ip}',end='\r')