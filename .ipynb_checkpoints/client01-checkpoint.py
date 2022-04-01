import sys
import socket
import logging

try :
    #create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IP = '172.16.16.101'
    PORT = 9999
    ADDR = (IP,PORT)

    #create connet
    client.connect(ADDR)

    #receiv data from server
    data = client.recv(1024)
    m = data.decode()

    print (m)
    
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
    
finally:
    logging.info("closing")
    client.close()