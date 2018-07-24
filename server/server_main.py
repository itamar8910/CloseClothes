import io
import json
import socket
import sys
from struct import pack, unpack
from threading import Thread
from typing import List

import numpy as np
from PIL import Image

from algorithm.bbox.bbox_heuristic import get_uperbody_bbox_from_npy
from database.TinyDB_DB import TinyDB_DB

sys.path.append("..")
SOCKET_SIZE = 10
PORT = 8080
NUM_NEIGHBORS = 3

db = TinyDB_DB()
def main():
    # handle_client(None) # TODO: remove
    # exit()
    sever_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sever_socket.bind(("",PORT))
    sever_socket.listen(SOCKET_SIZE)
    running = True
    while running:
        print("waiting for connection")
        client_socket, client_address = sever_socket.accept()
        handle_client(client_socket)
        client_thread = Thread(target=handle_client,args=(client_socket,))
        client_thread.start()

def handle_client(client_socket):
    """ Responds to a given socket"""
    print("Handling client:")
    def read_socket_bytes(message_length):
        """ reads `message_length` bytes from the client_socket"""
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
    
    def send_socket_bytes(message : bytes):
        """ Sends the message by first sending it's length, and then the message itself"""
        msg_length = pack('!i', len(message))
        client_socket.sendall(msg_length)
        client_socket.sendall(message)
    

    HEADER_SIZE = 4
    image_size = int(unpack('!i',read_socket_bytes(HEADER_SIZE))[0])
    image_bytes = read_socket_bytes(image_size)

    img = Image.open('tmp.png')    
    # img = Image.open(io.BytesIO(image_bytes))
    # img = img.rotate(-90, expand=1)

    img.show()
    PATH = 'tmp.png'
    img.save(PATH)
    # img.show()
    # feats = db.feat_extractor.get_feats([PATH])[0]
    K = 5
    # knn = db.knn(center=np.array(img), num_neighbors=NUM_NEIGHBORS)
    # knn_json = json.dumps(knn)
    return_dummy_result = False
    if return_dummy_result:
        knn_json = db.get_all()[:K]
        
        indicies = [0] * K
    else:  
        indicies, knn_json = db.knn(PATH, K)
    import tqdm
    for idx, neighbor in tqdm.tqdm(zip(indicies, knn_json), desc = "removing redundant features"):
        try:
            neighbor['img_index'] = idx
            del neighbor['feats']
        except KeyError:
            pass
    knn_json = json.dumps(knn_json, ensure_ascii=True)

    send_socket_bytes(bytes(knn_json, encoding='utf-8'))

if __name__ == '__main__':
    main()
