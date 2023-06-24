import socket
import os

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is listening for incoming connections on port", self.port, "with IP", self.server_socket.getsockname()[0])

        client_socket, addr = self.server_socket.accept()
        print("Connected to:", addr)

        # Receive the folder or file name
        is_folder = client_socket.recv(1).decode() == '1'
        name_size = int.from_bytes(client_socket.recv(4), "big")
        name = client_socket.recv(name_size).decode()

        if is_folder:
            self.receive_folder(client_socket, name)
        else:
            self.receive_file(client_socket, name)

        client_socket.close()
        self.server_socket.close()

    def receive_file(self, client_socket, file_name):
        try:
            with open(file_name, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

            print("File received successfully:", file_name)
        except IOError as e:
            print("An error occurred while receiving the file:", str(e))

    def receive_folder(self, client_socket, folder_name):
        try:
            os.makedirs(folder_name, exist_ok=True)

            while True:
                # Receive the file name
                file_name_size = int.from_bytes(client_socket.recv(4), "big")
                if file_name_size == 0:
                    break
                file_name = client_socket.recv(file_name_size).decode()

                # Receive and save the file
                self.receive_file(client_socket, os.path.join(folder_name, file_name))

            print("Folder received successfully:", folder_name)
        except IOError as e:
            print("An error occurred while receiving the folder:", str(e))
