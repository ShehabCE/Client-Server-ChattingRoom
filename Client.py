import socket, sys, select

# MAX BUFFER SIZE = 8192
# FIXED PORT FROM SERVER = 5555

def Main():
    Client_Name = input("Name of Chatter: ")
    # Host = input("Name of Host:")  #localhost
    # Port = input("Port:")          #Fixed Port = 5555
    Host = "localhost"
    Port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect to Chatting Server.
    try:
        s.connect((Host, Port))
        message = "Chatter["+Client_Name+"]"
        s.send(message.encode())
    except:
        print("Unable to connect to Chatting Server :(")
        sys.exit()
    print("Connected to Chatting Server! You can start sending messages!")
    sys.stdout.write("[Me]: ")
    sys.stdout.flush()

    while True:
        List_Of_Sockets = [sys.stdin, s]
        READ, WRITE, ERROR = select.select(List_Of_Sockets, [], [])

        for incoming_sock in READ:
            if incoming_sock == s:
                # Message coming from Chatting Server.
                data = incoming_sock.recv(8192).decode()
                if not data:
                    print("Disconnected from Chatting Server.")
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write("[Me]: ")
                    sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(Main())

