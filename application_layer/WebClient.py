#!/usr/bin python3

from socket import *
import sys


def main():
    if len(sys.argv) != 4:
        print("Usage: WebClient.py <server_host> <server_port> <filename> ")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Create a TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))
        print("Connected with the server.")

        # Prepare the HTTP GET request
        http_request = f"GET /{filename} HTTP/1.1\r\n"
        http_request += f"Host: {server_host}\r\n\r\n"

        # Send the request to the server
        client_socket.send(http_request.encode())

        # Receive the response to the server
        response = client_socket.recv(2048).decode()
        print("Server response:\n")
        print(response)
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    main()
