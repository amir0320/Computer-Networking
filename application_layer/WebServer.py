from socket import *
import threading


def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(2048).decode()
        print(message)
        filename = message.split()[1]
        print(f"requesting file: {filename}")

        with open(filename[1:], 'rb') as f:
            outputdata = f.read()
        print(outputdata)

        # Determine the content-type based on file extension
        if filename.endswith(".html"):
            contentType = "text/html"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            contentType = "image/jpeg"
        elif filename.endswith(".png"):
            contentType = "image/png"
        else:
            contentType = "application/octet-stream"

        # Send the HTTP header
        httpHeader = "HTTP/1.1 200 OK\r\n"
        httpHeader += f"Content-Length: {len(outputdata)}\r\n"
        httpHeader += f"Content-Type: {contentType}\r\n"
        httpHeader += "\r\n"

        connectionSocket.send(httpHeader.encode())

        # Send the content of the requested file to the client
        connectionSocket.send(outputdata)

    except IOError:
        # Send response message for file not found
        httpHeader = "HTTP/1.1 404 Not Found\r\n"
        errorMessage = "<html><body><h1>404 Not Found</h1></body></html>"
        httpHeader += f"Content-Length: {len(errorMessage)}\r\n"
        httpHeader += "Content-Type: text/html\r\n"
        httpHeader += "\r\n"
        connectionSocket.send(httpHeader.encode())
        connectionSocket.send(errorMessage.encode())
        print("404 Not Found")
    finally:
        # Close client socket
        connectionSocket.close()
        print("Client connection is closed.")


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverSocket.bind(('', serverPort))
serverSocket.listen(5)  # Allow up to 5 queued connections
print('The server is ready to receive...up to 5 connections')

try:
    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection established with {addr}")

        # Create a new thread to handle the client connetion
        clientThread = threading.Thread(target=handle_client,
                                        args=(connectionSocket, ))
        clientThread.start()  # Start the thread
except KeyboardInterrupt:
    print("Server is shutting up gracefully.")
except Exception as e:
    print("An error occurred: ", e)
finally:
    serverSocket.close()
    print("Server socket closed.")
