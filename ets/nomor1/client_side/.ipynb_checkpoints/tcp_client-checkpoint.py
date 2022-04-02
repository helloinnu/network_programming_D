import sys
import socket
import json
import logging
import xmltodict
import ssl
import os
import time
import datetime
import threading
import random
from tabulate import tabulate


IP = '172.16.16.101'
PORT = 12000
SERVER_ADDR = (IP, PORT)

def make_socket(SERVER_ADDR):
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        logging.warning(f"connecting to {SERVER_ADDR}")
        client_sock.connect(SERVER_ADDR)
        return client_sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def make_secure_socket(SERVER_ADDR):
    try:
        #get it from https://curl.se/docs/caextract.html

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/domain.crt')

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = (destination_address, port)
        logging.warning(f"connecting to {SERVER_ADDR}")
        client_sock.connect(SERVER_ADDR)
        secure_socket = context.wrap_socket(client_sock,SERVER_ADDR)
        logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(data):
    #logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(data)
    

def send_command(command_str,is_secure=False):

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # gunakan fungsi diatas
    if is_secure == True:
        client_sock = make_secure_socket(SERVER_ADDR)
    else:
        client_sock = make_socket(SERVER_ADDR)

    #logging.warning(f"connecting to {SERVER_ADDR}")
    try:
        logging.warning(f"sending message ")
        client_sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = client_sock.recv(16)
            # time.sleep(1)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    # end_time = datetime.datetime.now()
                    # timestamp = end_time - start_time
                    # print(f"Waktu TOTAL yang dibutuhkan {timestamp} detik ")    
                
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False



def getdatapemain(nomor=0,is_secure=False):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil


def getlistpemain(total_request, table_data):
    total_response = 0
    texec = dict()
    start_time = datetime.datetime.now()

    for k in range(total_request):
        # bagian ini merupakan bagian yang mengistruksikan eksekusi getdatapemain secara multithread
        texec[k] = threading.Thread(target=getdatapemain, args=(random.randint(1, 20),))
        texec[k].start()

    # setelah menyelesaikan tugasnya, dikembalikan ke main thread dengan join
    for k in range(total_request):
        if (texec[k]):
            total_response += 1
        texec[k].join()

    end_time = datetime.datetime.now()
    times = end_time - start_time
    table_data.append([total_request, total_request, total_response, times])

if __name__ == '__main__':

    total_request = [1, 5, 10, 20]
    tabel_matrik = []
    
    for request in total_request:
        getlistpemain(request, tabel_matrik)
        
    header = ["Jumlah Thread", "Jumlah Request", "Jumlah Response", "Latency"]
    print("")
    print(tabulate(tabel_matrik, headers=header))
