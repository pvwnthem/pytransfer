import socket
import os
import argparse

class FileSharerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def connect(self):
        self.socket.connect((socket.gethostname(), self.port))
        print("Connected to the server.")

    def send_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Send file metadata (name and size)
        self.socket.sendall(f"{file_name}|{file_size}".encode())

        # Send file content
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                self.socket.sendall(data)

        print(f"File '{file_name}' sent successfully.")

    def send_folder(self, folder_path):
        folder_name = os.path.basename(folder_path)

        # Send folder name
        self.socket.sendall(folder_name.encode())

        # Traverse the folder recursively and send files
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.send_file(file_path)

        print(f"Folder '{folder_name}' sent successfully.")

    def close(self):
        self.socket.close()
        print("Connection closed.")

class FileSharerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def start(self):
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.listen(1)
        print(f"Server started at {self.socket.getsockname()[0]}. Waiting for connections...")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection established with {client_address[0]}:{client_address[1]}")

            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        # Receive file or folder
        data = client_socket.recv(4096).decode()

        if "|" in data:
            # File transfer
            file_name, file_size = data.split("|")
            file_size = int(file_size)

            self.receive_file(client_socket, file_name, file_size)
        else:
            # Folder transfer
            folder_name = data
            self.receive_folder(client_socket, folder_name)

        client_socket.close()

    def receive_file(self, client_socket, file_name, file_size):
        received_bytes = 0

        # Create a new file to save the received data
        with open(file_name, "wb") as file:
            while received_bytes < file_size:
                data = client_socket.recv(4096)
                file.write(data)
                received_bytes += len(data)

        print(f"Received file '{file_name}'.")

    def receive_folder(self, client_socket, folder_name):
        # Create a new folder to save the received files
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        while True:
            # Receive files one by one
            data = client_socket.recv(4096).decode()

            if not data:
                break

            file_name, file_size = data.split("|")
            file_size = int(file_size)

            # Receive and save the file
            self.receive_file(client_socket, os.path.join(folder_name, file_name), file_size)

        print(f"Received folder '{folder_name}'.")

    def close(self):
        self.socket.close()
        print("Server closed.")

def run_client(host, port, files, folders):
    client = FileSharerClient(host, port)
    client.connect()

    for file_path in files:
        client.send_file(file_path)

    for folder_path in folders:
        client.send_folder(folder_path)

    client.close()

def run_server(host, port):
    server = FileSharerServer(host, port)
    server.start()

def main():
    parser = argparse.ArgumentParser(description="File Sharer CLI")
    parser.add_argument("-m", "--mode", choices=["client", "server"], required=True, help="Operating mode: client or server")
    parser.add_argument("-H", "--host", default="localhost", help="Host address")
    parser.add_argument("-p", "--port", type=int, default=12345, help="Port number")
    parser.add_argument("-f", "--files", nargs="+", help="Files to share")
    parser.add_argument("-d", "--folders", nargs="+", help="Folders to share")

    args = parser.parse_args()

    if args.mode == "client":
        if not args.files and not args.folders:
            parser.error("At least one file or folder must be specified for the client mode.")

        run_client(args.host, args.port, args.files, args.folders)
    else:
        run_server(args.host, args.port)

if __name__ == "__main__":
    main()
