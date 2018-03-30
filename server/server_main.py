import socket
from threading import Thread
from struct import pack,unpack
from PIL import Image
import io

SOCKET_SIZE = 10
PORT = 8080

def main():
    sever_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sever_socket.bind(("",PORT))
    sever_socket.listen(SOCKET_SIZE)
    running = True
    while running:
        client_socket, client_address = sever_socket.accept()
        client_thread = Thread(target=handle_client,args=(client_socket,))
        client_thread.start()

def handle_client(client_socket):
    print("Handling client:")
    def read_socket_bytes(message_length):
        chunks = []
        bytes_recd = 0
        while bytes_recd < message_length:
            try:
                chunk = client_socket.recv(min(message_length - bytes_recd, 2048))
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            except socket.error as error:
                if error == socket.EAGAIN or error == socket.EWOULDBLOCK:
                    continue
                else:
                    raise
        return  b''.join(chunks)

    HEADER_SIZE = 4
    image_size = int(unpack('!i',read_socket_bytes(HEADER_SIZE))[0])
    image_bytes = read_socket_bytes(image_size)
    print(type(image_bytes))
    print(len(image_bytes))
    Image.open(io.BytesIO(image_bytes)).show()

if __name__ == '__main__':
    main()