import socket, sys, select

#GLOBALS
HOST = ''               #Local Host.
LIST_OF_SOCKETS =[]     #Arrayy of Sockets connected from Clients.
RECV_BUFFER = 8192      #Maximum Buffer Size.
PORT = 5555             #Fixed Port Number.

# Broadcasts the Message to all Sockets in the List (Clients).
def broadcast_Message(Server_SOCK, BC_Message):
    for sock in LIST_OF_SOCKETS:
        #Allow the sender to see the broadcasted message too.
        if sock != Server_SOCK:
            try:
                sock.send(BC_Message).encode()
            except:
                #Socket Connection is broken, close it and remove it.
                sock.close()
                if sock in LIST_OF_SOCKETS:
                    LIST_OF_SOCKETS.remove(sock)


def Main():
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
            #New Connection Request from Client
            if incoming_SOCK == Server_SOCK:
                SOCKfd, addr = Server_SOCK.accept()
                LIST_OF_SOCKETS.append(SOCKfd)
                Server_msg = "Client [" + str(addr) + "] connected."
                print(Server_msg)
                Server_msg = "[" + str(addr) + "] entered our epic chatting room."
                broadcast_Message(Server_SOCK, Server_msg)
            #New Message from Client
            else:
                try:
                    data = incoming_SOCK.recv(RECV_BUFFER).decode()
                    if data:
                        #there is data in the buffer, broadcast it to all active clients.
                        Server_msg = "["+str(incoming_SOCK.getpeername())+"]: "+data
                        broadcast_Message(Server_SOCK, Server_msg)
                    else:
                        #The socket is broken, remove it.
                        if incoming_SOCK in LIST_OF_SOCKETS:
                            LIST_OF_SOCKETS.remove(incoming_SOCK)
                        #Inform Active Clients that this Client is offline.
                        Server_msg = "Client["+str(addr)+"] is offline."
                        broadcast_Message(Server_SOCK, Server_msg)

                except:
                    Server_msg = "Client["+str(addr)+"] is offline."
                    broadcast_Message(Server_SOCK, Server_msg)
                    continue
    Server_SOCK.close()


if __name__ == "__main__":
    sys.exit(Main())