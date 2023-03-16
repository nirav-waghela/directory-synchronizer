# # Nirav Waghela
# # Student Id : 1001919458

# import socket           # referred socket programming https://docs.python.org/3/howto/sockets.html
# import os               # os module gives method to get files and metadata of files in a specified directory
# import datetime         # datetime module converts unix code date to standard date time
# import shutil

# soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # initialized socket, it takes 2 argument INET and Streaming socket
# hostname = socket.gethostname()  # gets the address of localhost
# print('serverA started')
# server_a_port = 5252  # server A port
# server_b_port = 5454  # server B port


# soc2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # initialized socket for serverA to ServerB connection
# # soc2.bind((hostname,5454))
# soc.bind((hostname, server_a_port)) # connect to the server on port 5252

# # soc2.listen(20)
# soc.listen(15) # number of sockets that we can queue

# def checkFiles():
#     files = os.listdir(r"N:\directory_a") # listdir() list the files in the given directory
#     # print("files in server A directory", files)
#     filesMeta = []   # initialize an array that will store the metadata of files
#     for file in files: #iterate all the files in the given directory and get meta data of each file and convert them as per needed format
#         info = os.stat(r"N:/directory_a/" + file)  # referred https://docs.python.org/3/library/stat.html to get the metadata of the file
#         filesMeta.append("{}            {} kB          {}".format(file,str(int(info.st_size/1024)), datetime.datetime.utcfromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')))
#     return filesMeta

# while True:
#     clientsocket, address = soc.accept() # accept the connection from the client i.e connects client and serverA
#     print('Connection established with client')
#     files = os.listdir(r"N:\directory_a") # listdir() list the files in the given directory
#     # print("files in server A directory", files)
#     filesMeta = []   # initialize an array that will store the metadata of files
#     for file in files: #iterate all the files in the given directory and get meta data of each file and convert them as per needed format
#         info = os.stat(r"N:/directory_a/" + file)  # referred https://docs.python.org/3/library/stat.html to get the metadata of the file
#         filesMeta.append("{}            {} kB          {}".format(file,str(int(info.st_size/1024)), datetime.datetime.utcfromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')))


#     StrCov = '\n'.join([str(elem) for elem in filesMeta])


#     soc2.connect((hostname,server_b_port)) #connect serverA to serverB using connect()


#     # soc2.send(StrCov.encode())
#     # time.sleep(3)


#     msg= soc2.recv(1024) # received the data sent from serverB to serverA
#     print(msg)
#     # decode the data sent from serverB to serverA
#     for ele in str.splitlines(msg.decode('utf-8')): # format the data from serverB and append that data to the serverA data
#         filesMeta.append(ele)
#     filesMeta.sort()  #sorts the composite data of both the servers according to the name of the file in ascending order
#     # print(filesMeta,"====================")
#     covStr = '\n'.join([str(elem) for elem in filesMeta]) # convert the sorted data into string using join() and send the sorted data to client
#     soc2.send(covStr.encode())
#     print(covStr,"Files synced")
#     clientsocket.send(covStr.encode())  # data is being encoded and then send to client using send()


import os
import json
import socket
from server import *
import asyncio
from utils import *


def sub_task():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9998))
    s.send(b'list')
    data = s.recv(1024).decode("utf-8")
    return json.loads(data)


def server_a_list_files(c, directory):
    files = get_metadata_for_directory(directory)
    server_b_files = sub_task()
    if len(server_b_files) > 0:
        files.extend(server_b_files)
    c.send(json.dumps(files).encode("utf-8"))


serviceA = Service('Server A', './test-dir/', 9999, 9998)
serviceA.register_command_handler('list', server_a_list_files)
serviceA.register_command_handler('sync', sync_handler)

# refernce to run multiple tasks until completion

# https://stackoverflow.com/a/48566118
# reference for handling ctrl c for asyncio
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serviceA.start())

except KeyboardInterrupt:
    print('\nShutting down server')
    serviceA.stop()
    loop.close()
    print('Server shut down')
    os._exit(0)
