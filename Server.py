import socket, sys, select

#GLOBALS
HOST = ''   #Local Host
LIST_OF_SOCKETS =[]     #Arrayy of Sockets reached
RECV_BUFFER = 8192
PORT = 5555

def chat_manager():
    Server_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Server_SOCK.bind((HOST, PORT))
    #Server can receive up to 25 Client Connections.
    Server_SOCK.listen(25)

    LIST_OF_SOCKETS.append(Server_SOCK)
    Server_msg = "Chat Server running on :"+str(PORT)
    print(Server_msg)

    while True:
        READ, WRITE, ERROR = select.select(LIST_OF_SOCKETS, [], [], 0)

        for incoming_SOCK in READ:
            #New Connection Request Read
            if incoming_SOCK == Server_SOCK:
                SOCKfd, addr = Server_SOCK.accept()
                LIST_OF_SOCKETS.append(SOCKfd)
                Server_msg = "Client (" + addr + ") connected."
                print(Server_msg)
                broadcast
