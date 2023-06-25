import tkinter as tk
from tkinter import messagebox
import argparse
from src.server.server import Server
from src.client.client import Client

def start_program(mode, ip, file, root):
    if mode == 'server':
        server = Server()
        root.destroy()
        server.run()
          # Close the window when the server is started
    elif mode == 'client':
        if not ip or not file:
            messagebox.showerror("Error", "Both IP and File fields are required for client mode.")
            return

        client = Client(ip, file)
        client.run()

def main():
    def start_button_click():
        mode = mode_var.get()
        ip = ip_entry.get()
        file = file_entry.get()
        start_program(mode, ip, file, root)

    root = tk.Tk()
    root.title("File Transfer Program")
    root.geometry("240x360")

    mode_label = tk.Label(root, text="Mode:")
    mode_label.pack()

    mode_var = tk.StringVar()
    mode_var.set("client")

    mode_radio_client = tk.Radiobutton(root, text="Client", variable=mode_var, value="client")
    mode_radio_client.pack()

    mode_radio_server = tk.Radiobutton(root, text="Server", variable=mode_var, value="server")
    mode_radio_server.pack()

    ip_label = tk.Label(root, text="IP:")
    ip_label.pack()

    ip_entry = tk.Entry(root)
    ip_entry.pack()

    file_label = tk.Label(root, text="File:")
    file_label.pack()

    file_entry = tk.Entry(root)
    file_entry.pack()

    start_button = tk.Button(root, text="Start", command=start_button_click)
    start_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
