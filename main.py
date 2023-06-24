import argparse
from src.server.server import Server
from src.client.client import Client

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Transfer Program')
    parser.add_argument('mode', choices=['client', 'server'], help='Choose "client" or "server" mode')
    parser.add_argument('-i', '--ip', help='Specify the server IP address')
    parser.add_argument('-p', '--path', help='Specify the file or folder path')

    args = parser.parse_args()

    if args.mode == 'server':
        server = Server()
        server.run()
    elif args.mode == 'client':
        if not args.ip or not args.path:
            parser.error("For client mode, both --ip and --path are required.")
        client = Client(args.ip, args.path)
        client.send()