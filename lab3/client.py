import socket
import threading
import sys
from stream import StreamCipher
from mh import *
import ast
import random
import string

class Client:
    def __init__(self, host, port, id):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher = StreamCipher()
        self.id = id
        self.priv_key, self.pub_key = generate_knapsack_key_pair()
        print(f"Client created with priv key {self.priv_key}; pub key {self.pub_key}")

    def convert_str_to_tuple(self, tuple_string):
        return ast.literal_eval(tuple_string.decode('utf-8'))
    
    def generate_random_sequence(self):
        length = random.randint(3, 10)  # Adjust the range as needed

        # Generate a random sequence of characters and numbers
        characters_and_numbers = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters_and_numbers) for _ in range(length))

        return random_string
    
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
        print("Connected to keyserver")

        msg = str(self.id) + "-" + str(self.pub_key)
        self.client_socket.send(msg.encode())

        msg = input("Enter your message: ")
        self.client_socket.send(msg.encode())
        print(f"msg {msg} sent")

        try:
            print("trying to get pub key")
            data = self.client_socket.recv(1024)
            if not data:
                print("Something went wrong - no data")

            print(f"Received: {data}")

        except Exception as e:
            print(f"Error receiving data: {e}")

        self.pub_key_other = data
        print(f"The other clients public key is : {self.pub_key_other}")

        #sending the hello msg
        msg = input("Enter your message: ")
        self.client_socket.send(msg.encode())
        print(f"msg {msg} sent")

        #getting the hello msg
        data = self.client_socket.recv(1024)
        data = ast.literal_eval(data.decode('utf-8'))
        print(f"The other client says {decrypt_mh(data, self.priv_key)}")

        random_secret = self.generate_random_sequence()
        print(random_secret)
        random_secret = "semmi"

        # sending a half of the secret
        id_secret = str(self.id) + str(random_secret)
        id_secret = "semmi"
        print(f"id secret {id_secret}")
        id_secret = str(encrypt_mh(id_secret, self.pub_key_other))
        print(f"encrypted id_secret {id_secret}")
        self.client_socket.send(id_secret.encode('utf-8'))
        print(f"msg {id_secret} sent")

        # receiving the half secrets
        data = self.client_socket.recv(1024)
        print(f"data received {data}")
        msg = ast.literal_eval(data.decode('utf-8'))
        print(f"list data {data}")
        msg = decrypt_mh(msg, self.priv_key)
        print(f"decrypted {msg}")

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        

        while True:
            
            message = input("Enter your message: ")
            encrypted_message = self.cipher.encrypt(message)
            self.client_socket.send(encrypted_message)

if __name__ == "__main__":
    client = Client('127.0.0.1', 8001, sys.argv[1])
    client.start()
