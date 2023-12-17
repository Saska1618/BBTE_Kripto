import socket
from stream_cipher.general_stream_cipher import GeneralStreamCipher


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print(f'Connected to {server_address[1]}...')

    stream_cipher = GeneralStreamCipher('configs/blum_blum_config.json')

    try:
        while True:
            # Read a message from the user
            print('-'*50)
            message = input("Message: ")
            encrypted_message = stream_cipher.encrypt(message)
            print("Encrypted message:", encrypted_message)

            client_socket.sendall(encrypted_message.encode())

            # Receive the server's response
            data = client_socket.recv(1024)
            if not data:
                break

            received_message = data.decode()
            print("Received encoded message:", received_message)
            print("Decoded message:", stream_cipher.decrypt(received_message))
            print('-'*50)
    finally:
        # Clean up the connection
        client_socket.close()


if __name__ == "__main__":
    client()
