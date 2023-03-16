import socket
import sys
from _thread import *
import threading
 
# Data to be written

userData = {}

thread_lock = threading.Lock()

def server_connection():
    HOST, PORT = '127.0.0.1', 8037

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as err:
        print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
        sys.exit()

    s.listen(10)
    print ('Server has started')


    while True:
        conn, address = s.accept()
        thread_lock.acquire()
        print ('Connect with ' + address[0] + ':' + str(address[1]))
        start_new_thread(userTasks, (conn,))
    s.close()


def userTasks(c):
    while True:
        message = c.recv(1024).decode('utf-8')
        print(message)
        data = message.split()
        if data[0] == 'PUT' or data[0] =='put':
            nameType,value = data[1],data[-1]
            userData[nameType] = value
            c.send(b"Added to the list")

        if data[0] == 'GET' or data[0] =='get':
            nameType = data[1]
            requested_data = userData[nameType]
            print(requested_data)
            c.send(requested_data.encode('utf-8'))
            
        
        if data[0] == 'DUMP' or data[0] == 'dump':
            requested_data = str(list(userData.keys()))
            print(requested_data)
            c.send(requested_data.encode('utf-8'))


if __name__ == '__main__':
    server_connection()

