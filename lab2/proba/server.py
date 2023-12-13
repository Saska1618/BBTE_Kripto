import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")

    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {addr}: {message}")
            
            # Broadcast the message to all connected clients
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except socket.error as e:
                        print(f"Error broadcasting message to a client: {e}")

            if message == 'exit':
                break

        except socket.error as e:
            print(f"Error receiving message from {addr}: {e}")
            break

    print(f"Connection from {addr} closed.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    host = '127.0.0.1'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
