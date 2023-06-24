import socket
import os

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999

    def receive_file(self, client_socket):
        file_name_size = int.from_bytes(client_socket.recv(4), "big")
        file_name = client_socket.recv(file_name_size).decode("utf-8")
        print(file_name)
        try:
            with open(file_name, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print("nd")
                        break
                    file.write(data)

            print("File received successfully:", file_name)
        except IOError as e:
            print("An error occurred while receiving the file:", str(e))

    def receive_folder(self, client_socket):
        folder_name = client_socket.recv(1024).decode("utf-8")
        print(folder_name)

        try:
            os.mkdir(folder_name)
        except FileExistsError:
            print("unstuck err")
            pass

        os.chdir(folder_name)

        while True:
            self.receive_file(client_socket)
            print("unstuck")
            client_socket.send(b"ACK")  # Send acknowledgement to client

            # Check if all files have been received
            data = client_socket.recv(1024)
            print(data, "rc")
            if data == b"DONE":
                break

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
                print("wtf")
                break

            if data == b"FILE":
                print("fg=ile")
                self.receive_file(client_socket)
                print("fg=ile")
            elif data == b"FOLDER":
                print("fg=older")
                self.receive_folder(client_socket)
                print("fg=older")

        client_socket.close()
        self.server_socket.close()
