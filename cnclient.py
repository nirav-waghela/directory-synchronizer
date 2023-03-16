
import socket

hostname,port = "127.0.0.1",8037

cache = {}

client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname, port))
while True:
    print("Select either of one: PUT GET DUMP")
    userInput=input('')
    data = userInput.split(' ')
    if data[0] == 'GET' or data[0] =='get':
        if data[1] in cache:
            print('From proxy server: ',cache[data[1]])
        cache[data[1]] = ''
        client.send(userInput.encode("utf-8"))
        print("Request Forwarded to Server")
        message = client.recv(1024).decode("utf-8")
        cache[data[1]] = message
        print("Response from server: ",message)
    else:
        client.send(userInput.encode("utf-8"))
        print("Request Forwarded to Server")
        message = client.recv(1024).decode("utf-8")
        print("Response from server: ",message)
client.close()
