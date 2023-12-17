import socket
from stream_cipher.general_stream_cipher import GeneralStreamCipher


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    server_socket.listen(1)     # Accept at most 1 connection
    print(f"Server listening on port {server_address[1]}...")

    # Accept a connection
    connection, client_address = server_socket.accept()
    print("Connection from", client_address)

    stream_cipher = GeneralStreamCipher('configs/blum_blum_config.json')

    try:
        while True:
            # Receive data from the client
            data = connection.recv(1024)
            if not data:
                break

            print('-'*50)
            received_message = data.decode()
            print("Received encoded:", received_message)
            print("Decoded:", stream_cipher.decrypt(received_message))

            # Send a response back to the client
            response = input("Message: ")
            encrypted_response = stream_cipher.encrypt(response)
            print("Encrypted:", encrypted_response)
            connection.sendall(encrypted_response.encode())
            print('-'*50)
    finally:
        # Clean up the connection
        connection.close()


if __name__ == "__main__":
    server()
