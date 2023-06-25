import socket
import os

class Client:
    def __init__(self, ip, path):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = 9999
        self.path = path

    def send_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        self.client_socket.sendall(file_size.to_bytes(8, "big"))  # Send file size

        try:
            with open(file_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    self.client_socket.sendall(data)
                    data = file.read(1024)

            print("File sent successfully:", file_name)
        except IOError as e:
            print("An error occurred while sending the file:", str(e))

    def send_folder(self, folder_path):
        folder_name = os.path.basename(folder_path)
        self.client_socket.send(folder_name.encode())

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.send_file(file_path)

    def run(self):
        try:
            self.client_socket.connect((self.ip, self.port))

            if os.path.isfile(self.path):
                self.send_file(self.path)
            elif os.path.isdir(self.path):
                self.send_folder(self.path)
            else:
                print("Invalid path:", self.path)
                return

        except ConnectionRefusedError:
            print("Failed to connect to the peer:", self.ip)
        finally:
            self.client_socket.close()