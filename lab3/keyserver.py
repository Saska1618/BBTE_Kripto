import socket
import threading

from mh import *
import ast

def str_to_tuple(tuple_string):
    return ast.literal_eval(tuple_string)

def handle_client(client_socket, address):

    data = client_socket.recv(1024)
    print(f'data from {address} : {data}')
    cid, pub_key = data.decode().split('-')
    id_pub[cid] = pub_key

    print(f'client with id {cid} registered')


    while True:
        print("Start of while")
        try:
            data = client_socket.recv(1024)
            if type(data) != 'str':
                data = data.decode()
            print(data)
            
            
            if data == 'get':
                for clid, clkey in id_pub.items():
                    print(clid, cid)
                    if clid != cid:
                        msg = id_pub[clid]
                        break
                msg = msg.encode()

                for c in clients:
                    if c == client_socket:
                        c.send(msg)
                        print(f"msg {msg} sent to {c}")
            else:

                if data == 'sendHello':
                    for clid, clkey in id_pub.items():
                        print(clid, cid)
                        if clid != cid:
                            tup_pub_key = str_to_tuple(id_pub[clid])
                            msg = str(encrypt_mh('hello', tup_pub_key))
                            print(f"encrypted msg {msg}")
                            break
                    msg = msg.encode()
                else:
                    msg = data.encode()
                    print(f"data {type(data)}")
                    
                
                for c in clients:
                    if c != client_socket:
                        c.send(msg)
                        print(f"msg {msg} sent to {c}")

            

            
        except Exception as e:
            print(f"Error handling client {cid}: {e}")
            break

def start_server():
    host = '127.0.0.1'
    port = 8001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print('Keyserver started')

    while True:
        client_socket, address = server_socket.accept()
        print(f"client connected on addr: {address}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    clients = []
    id_pub = {}
    start_server()
