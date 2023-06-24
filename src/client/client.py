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
        file_name_size = len(file_name)
        self.client_socket.send(b'0')  # Send flag indicating a file
        self.client_socket.send(file_name_size.to_bytes(4, "big"))
        self.client_socket.send(file_name.encode())

        try:
            with open(file_path, 'rb') as file:
                for data in file:
                    self.client_socket.send(data)

            print("File sent successfully:", file_name)
        except IOError as e:
            print("An error occurred while sending the file:", str(e))

    def send_folder(self, folder_path):
        folder_name = os.path.basename(folder_path)
        folder_name_size = len(folder_name)
        self.client_socket.send(b'1')  # Send flag indicating a folder
        self.client_socket.send(folder_name_size.to_bytes(4, "big"))
        self.client_socket.send(folder_name.encode())

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.send_file(file_path)

        # Send a zero-length file name to indicate the end of the folder
        self.client_socket.send(b'\x00\x00\x00\x00')

    def receive_data(self, size):
        data = b""
        while len(data) < size:
            packet = self.client_socket.recv(size - len(data))
            if not packet:
                break
            data += packet
        return data

    def receive_file_name(self):
        name_size = int.from_bytes(self.receive_data(4), "big")
        file_name = self.receive_data(name_size).decode()
        return file_name

    def send(self):
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

        self.client_socket.close()
