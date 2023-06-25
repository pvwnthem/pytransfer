import socket
import errno
import os

class Server:
    def __init__(self, destination_folder):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999
        self.destination_folder = destination_folder

    def run(self):
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is listening for incoming connections on port", self.port, "with IP", self.server_socket.getsockname()[0])

        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print("Connected to:", addr)
                break
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    print("An error occurred while accepting a connection:", str(e))
                    return

        file_name_size = int.from_bytes(client_socket.recv(4), "big")
        file_name = client_socket.recv(file_name_size).decode()
        destination_path = os.path.join(self.destination_folder, file_name)

        try:
            with open(destination_path, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

            print("File received successfully:", destination_path)
        except IOError as e:
            print("An error occurred while receiving the file:", str(e))

        client_socket.close()
        self.server_socket.close()
