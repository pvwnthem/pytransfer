import socket
import os

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999

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
            os.mkdir(folder_name)
        except FileExistsError:
            pass

        os.chdir(folder_name)

        while True:
            file_name_size = int.from_bytes(client_socket.recv(4), "big")
            file_name = client_socket.recv(file_name_size).decode("utf-8")

            if file_name == "DONE":
                break

            self.receive_file(client_socket, file_name)
            client_socket.send(b"ACK")

        os.chdir("..")

        print("Folder received successfully:", folder_name)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is listening for incoming connections on port", self.port, "with IP", self.server_socket.getsockname()[0])

        client_socket, addr = self.server_socket.accept()
        print("Connected to:", addr)

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            if data == b"FILE":
                file_name_size = int.from_bytes(client_socket.recv(4), "big")
                file_name = client_socket.recv(file_name_size).decode("utf-8")
                self.receive_file(client_socket, file_name)
            elif data == b"FOLDER":
                folder_name_size = int.from_bytes(client_socket.recv(4), "big")
                folder_name = client_socket.recv(folder_name_size).decode("utf-8")
                self.receive_folder(client_socket, folder_name)

        client_socket.close()
        self.server_socket.close()
