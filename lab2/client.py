import socket
import threading
from stream import StreamCipher

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher = StreamCipher()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                #print(type(data))
                decrypted_data = self.cipher.decrypt(data.decode())

                print(f"Received: {decrypted_data}")

            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def start(self):
        self.client_socket.connect((self.host, self.port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            
            message = input("Enter your message: ")
            encrypted_message = self.cipher.encrypt(message)
            self.client_socket.send(encrypted_message)

if __name__ == "__main__":
    client = Client('127.0.0.1', 5555)
    client.start()
