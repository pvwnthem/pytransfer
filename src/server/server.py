import socket

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is listening for incoming connections on port", self.port, " with ip ", self.server_socket.getsockname()[0])

        client_socket, addr = self.server_socket.accept()
        print("Connected to:", addr)

        file_name_size = int.from_bytes(client_socket.recv(4), "big")
        file_name = client_socket.recv(file_name_size).decode()

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

        client_socket.close()
        self.server_socket.close()
