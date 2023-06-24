import socket
import os

# Server IP and port
SERVER_IP = '127.0.0.1'  # Change this to the server IP
SERVER_PORT = 12345  # Change this to the server port

# Buffer size for sending/receiving data
BUFFER_SIZE = 4096


def send_file(sock, file_path):
    """
    Send a file over the socket.
    """
    file_name = os.path.basename(file_path)
    sock.send(file_name.encode())

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            sock.sendall(data)

    print(f"File '{file_name}' sent successfully.")


def receive_file(sock):
    """
    Receive a file from the socket.
    """
    file_name = sock.recv(BUFFER_SIZE).decode()

    with open(file_name, 'wb') as file:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)

    print(f"File '{file_name}' received successfully.")


def send_folder(sock, folder_path):
    """
    Send a folder over the socket.
    """
    folder_name = os.path.basename(folder_path)
    sock.send(folder_name.encode())

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as file:
                sock.send(file_name.encode())

                while True:
                    data = file.read(BUFFER_SIZE)
                    if not data:
                        break
                    sock.sendall(data)

    print(f"Folder '{folder_name}' sent successfully.")


def receive_folder(sock):
    """
    Receive a folder from the socket.
    """
    folder_name = sock.recv(BUFFER_SIZE).decode()
    os.makedirs(folder_name, exist_ok=True)

    while True:
        file_name = sock.recv(BUFFER_SIZE).decode()
        if not file_name:
            break

        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'wb') as file:
            while True:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)

    print(f"Folder '{folder_name}' received successfully.")


def start_server():
    """
    Start the file transfer server.
    """
    print("Starting server...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)

    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")

        while True:
            choice = client_socket.recv(BUFFER_SIZE).decode()

            if choice == '1':
                receive_file(client_socket)
            elif choice == '2':
                receive_folder(client_socket)
            elif choice == '3':
                client_socket.close()
                print(f"Client disconnected: {client_address}")
                break
            else:
                print("Invalid choice. Please try again.")

    server_socket.close()


def start_client():
    """
    Start the file transfer client.
    """
    print("Starting client...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    while True:
        print("\nMenu:")
        print("1. Send a file")
        print("2. Send a folder")
        print("3. Quit")

        choice = input("Enter your choice: ")

        client_socket.send(choice.encode())

        if choice == '1':
            file_path = input("Enter the file path: ")
            send_file(client_socket, file_path)
        elif choice == '2':
            folder_path = input("Enter the folder path: ")
            send_folder(client_socket, folder_path)
        elif choice == '3':
            client_socket.close()
            break
        else:
            print("Invalid choice. Please try again.")

    print("Client closed.")


def main():
    """
    Entry point of the program.
    """
    print("Welcome to FileTransfer!")

    while True:
        print("\nMenu:")
        print("1. Start server")
        print("2. Start client")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            start_server()
        elif choice == '2':
            start_client()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    print("Goodbye!")


if __name__ == '__main__':
    main()
