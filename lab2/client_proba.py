import socket
from stream import generate_keystream_solitaire, blum_blum_shub, StreamCipher

def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen(1)
    print("Server is listening for connections...")
    return s

def communicate(conn, cipher):
    while True:
        data = conn.recv(1024)
        print("Listening")
        if not data:
            break
        decrypted_data = cipher.decrypt(data.decode())
        print(f"Received: {decrypted_data}")

        message = input("Enter your message: ")
        encrypted_message = cipher.encrypt(message)
        conn.send(encrypted_message.encode())

def main():
    
    cipher = StreamCipher()

    server_socket = init_socket()
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    communicate(conn, cipher)

    conn.close()

if __name__ == "__main__":
    main()
