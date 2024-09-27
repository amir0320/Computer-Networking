from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# set to keep track of clients who have already received the greeting
clients_greeted = set()

try:
    hostname = gethostname()
    ip_address = gethostbyname(hostname)

    # assign port number 12000 to the server's socket
    serverSocket.bind(('', serverPort))
    print("The server is ready to receive...")

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()

        if clientAddress not in clients_greeted:
            selfIntro = ("Hello, this is {} from {}. {}"
                .format(hostname,ip_address,modifiedMessage))
            serverSocket.sendto(selfIntro.encode(), clientAddress)
            clients_greeted.add(clientAddress)
        else:
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)

except KeyboardInterrupt:
    print("Server is shutting down gracefully.")
except Exception as e:
    print("An error occurred:", e)
finally:
    serverSocket.close()
    print("Server socket closed.")
    print(clients_greeted)