import socket
import threading

def handle_client(client_socket, address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Broadcast the message to all clients
            for c in clients:
                if c != client_socket:
                    c.send(data)
        except Exception as e:
            print(f"Error handling client: {e}")
            break

def start_server():
    host = '127.0.0.1'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    clients = []
    start_server()
