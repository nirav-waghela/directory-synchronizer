# # Nirav Waghela
# # Student Id : 1001919458

# import socket                # referred socket programming https://docs.python.org/3/howto/sockets.html
# import os                    # os module gives method to get files and metadata of files in a specified directory
# import datetime              # datetime module converts unix code date to standard date time

# soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # initialized socket for serverA to ServerB connection
# hostname = socket.gethostname()   # gets the address of localhost
# soc.bind((hostname,5454))  # connect to the server on port 5454
# print('serverB started')


# # soc2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #initialized socket from serverB to ServerA connection

# soc.listen(20)  # number of sockets that we can queue

# def checkFiles ():
#     dir_data = os.listdir(r"N:\directory_b")
#     filesMeta = []   # initialize an array that will store the metadata of files
#     for file in os.listdir(r"N:\directory_b"):     # iterate all the files in the given directory and get meta data of each file and convert them as per needed format
#         info = os.stat(r"N:/directory_b/" + file)  # referred https://docs.python.org/3/library/stat.html to get the metadata of the file
#         filesMeta.append("{}            {} kB          {}".format(file,str(int(info.st_size/1024)), datetime.datetime.utcfromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')))
#     covStr = '\n'.join([str(elem) for elem in filesMeta])  # convert the data into string using join() and send the sorted data to serverA
#     print(covStr)
#     return (covStr)

# while True:
#     clientsocket, address = soc.accept()  # accept the connection from the client i.e connects serverA and serverB
#     # serverSocketA , address1 = soc2.accept() #accept the connection from serverA
#     # soc.connect((hostname,5252))
#     print('connection established with server A')

#     # print(soc.recv(1024),"data received from serverA")
#     fileData = checkFiles()
#     print(fileData)

#     clientsocket.send(fileData.encode())     # data is being encoded and then send to serverA using send()


import os
import json
import socket

from server import *
import asyncio
from utils import *


def server_b_list_files(c, directory):
    files = get_metadata_for_directory(directory)
    c.send(json.dumps(files).encode("utf-8"))


serviceB = Service('Server B', './test_dir_2/', 9998, 9999)
serviceB.register_command_handler('list', server_b_list_files)
serviceB.register_command_handler('sync', sync_handler)


# https://stackoverflow.com/a/48566118
# reference for handling ctrl c for asyncio

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serviceB.start())
except KeyboardInterrupt:
    print('\nShutting down server')
    serviceB.stop()
    loop.close()
    print('Server shut down')

    import os
    os._exit(0)
