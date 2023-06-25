# PyTransfer is currently a very heavy WIP. It has a partial amount of it's planned features currently active and it only works on some systems. If it works for you it is safe to use.

# PyTransfer

PyTransfer is a Python-based file transfer program that allows you to send files or folders between two computers using sockets.

## Usage

### Server

To run the server and listen for incoming connections:

python main.py server


### Client

To send a file to the server:

python main.py client -i SERVER_IP_ADDRESS -f FILE_PATH

To send a folder to the server:

python main.py client -i SERVER_IP_ADDRESS -f FOLDER_PATH


## Command-Line Options

The following options are available for the client mode:

| Option          | Description                                      |
|-----------------|--------------------------------------------------|
| `-i`, `--ip`    | Specify the server IP address                     |
| `-f`, `--file`  | Specify the file or folder path to send           |

## Requirements

- Python 3.x

## License

This project is licensed under the MIT License.

Please note that in the command-line options table, replace 'SERVER_IP_ADDRESS', 'FILE_PATH', and 'FOLDER_PATH' with appropriate values