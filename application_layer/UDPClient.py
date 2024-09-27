from socket import *

serverName = '192.168.5.6'
serverPort = 12000

# AF_INEF indicates its using IPv4
# SOCK_DGRAM means its a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        message = input("Input lowercase sentence:")
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

        print(modifiedMessage.decode())
except KeyboardInterrupt:
    print("Client was terminated by user.")
finally:
    clientSocket.close()
