
import socket  # referred socket programming https://docs.python.org/3/howto/sockets.html
import json

# initialized socket, it takes 2 argument INET and Streaming socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('localhost', 9999))

soc.send('list'.encode('utf-8'))

files = soc.recv(10240).decode('utf-8')

files = json.loads(files)
for file in files:
    # tabular format
    print(
        f"Name: {file['name']}\n\tSize(kb): {file['size_in_kb']}kb\n\tLast Modified: {file['modified time']}")

print("")
