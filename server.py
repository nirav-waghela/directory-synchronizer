
import json
import os
import socket
import threading
import time


def get_metadata(directory, file) -> dict:
    # get metadata for a file
    return{
        "name": file,
        "size_in_kb": os.path.getsize(os.path.join(directory, file)) / 1000,
        "modified": os.path.getmtime(os.path.join(directory, file)),
        "modified time": time.ctime(os.path.getmtime(os.path.join(directory, file))),
        "data": get_all_data_from_file(os.path.join(directory, file))
    }


def get_metadata_for_directory(directory) -> list:
    return [get_metadata(directory, file) for file in os.listdir(directory)]


def get_all_data_from_file(file) -> bytes:
    # read file contents
    with open(file, "r") as f:
        return f.read()


def create_socket(port):
    # function to create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port))
    s.listen(5)
    return s


def sync_handler(c, directory) -> None:
    # function to handle sync command received from some other server

    # create file helper
    def create_file(directory, name, data) -> None:
        with open(os.path.join(directory, name), 'w') as f:
            f.write(data)
            f.close()

    # get list of files on current server
    dir_list = os.listdir(directory)
    # get list of other server
    other_files = json.loads(c.recv(10240).decode("utf-8"))

    # create file if not exists
    for file in other_files:
        # print(file)
        # if file is not in current server, create it
        if file['name'] not in dir_list:
            print(f"Creating file {file['name']}")
            create_file(directory, file['name'], file['data'])

        # if file exists, compare with what is received, take recently modified
        elif file['name'] in dir_list:
            file_metadata = get_metadata(directory, file['name'])
            if (file_metadata['modified'] + 5) < file['modified']:
                print(f"Creating file {file['name']}")
                create_file(directory, file['name'], file['data'])


class Service:
    # class to run the server
    def __init__(self, name, dir, port, other_server_port):
        self.name = name
        self.dir = dir
        self.port = port
        self.running = False
        self.command_handlers = {}
        self.old_files = []
        self.other_server_port = other_server_port

    def print_log(self, message):
        print(f"{self.name}: {message}")

    # add command handler to dictionary
    def register_command_handler(self, command, handler):
        if command in self.command_handlers:
            raise Exception("Command already registered")
        self.command_handlers[command] = handler
        self.print_log(f"Registered command {command}")

    async def start(self):
        self.running = True
        threading.Thread(target=self._sync).start()
        self._run()

    def _sync(self):
        while True:
            time.sleep(3)
            files = get_metadata_for_directory(self.dir)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', self.other_server_port))
            s.send(b"sync")
            time.sleep(0.2)
            s.send(json.dumps(files).encode("utf-8"))

    def _wait_for_connection(self, s) -> (socket.socket, str):
        s.settimeout(5)
        try:
            c, addr = s.accept()
            return c, str(addr)
        except socket.timeout:
            return None, ''

    def _get_command(self, c) -> str:
        # initialize to null
        command = None
        # try to get command every second
        c.settimeout(1)
        # while command is null
        while command is None:
            try:
                command = c.recv(1024).decode("utf-8")
            except socket.timeout:
                pass
        # return trimmed command
        return command.strip()

    def _handle_command(self, c, command) -> None:
        # invoke command handler if registered
        if command in list(self.command_handlers.keys()):
            self.command_handlers[command](c, self.dir)
        else:
            self.print_log(f"Invalid command {command}")
            c.send(b"Invalid command")

    def _handle_connection(self, c) -> None:
        # for every new connection, get command and handle it and close connection
        command = self._get_command(c)
        self.print_log(f"Received command: {command}")
        self._handle_command(c, command)
        c.close()

    def _run(self) -> None:
        s = create_socket(self.port)
        self.print_log("Server Started")

        # while server is running
        # accept connection and handle it in new thread

        while self.running:
            # establish a connection
            c, addr = self._wait_for_connection(s)
            if c is None:
                self.print_log("No connection")
                continue
            self.print_log(f"Connected to {addr}")

            # handle connection in separate thread
            threading.Thread(target=self._handle_connection, args=(c,)).start()

        s.close()
        self.print_log("Server Stopped")

    def stop(self):
        self.running = False
