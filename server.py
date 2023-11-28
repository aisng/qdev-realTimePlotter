import socket
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Tuple, Union

from matplotlib import animation
from matplotlib.animation import FuncAnimation

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 10
MSG_START_ID = b"+++"
MSG_END_ID = b"---"
OK = "OK"
ERROR = "ERROR"


def initiate_plot(title: str = "Data", x_label: str = "x", y_label: str = "y") -> None:
    """Initiate the plot for data visualisation"""

    for elem in (title, x_label, y_label):
        if not isinstance(elem, str):
            raise TypeError(f"expected type str, got {type(elem)}", )

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def update_plot(x: int, y: int) -> None:
    """Update the plot with coordinates parsed from client's message"""

    for elem in (x, y):
        if not isinstance(elem, int):
            raise TypeError(f"expected type int, got {type(elem)}", )

    plt.plot(x, y, "bo", linewidth=2, markersize=3)
    plt.pause(0.1)


def find_pattern(data: Union[str, bytes], pattern: Union[str, bytes]) -> Tuple[bool, int]:
    """Find an element or a pattern in a string or bytestring object"""
    for elem in (data, pattern):
        if not isinstance(elem, (str, bytes)):
            raise TypeError("data and pattern must be of type str or bytes")

    if not isinstance(data, type(pattern)):
        raise TypeError("data and pattern must be of the same type")

    if len(data) < len(pattern):
        raise Exception("pattern length must not exceed data length")

    for i in range(len(data) - len(pattern) + 1):
        if data[i:i + len(pattern)] == pattern:
            return True, i
    return False, -1


def handle_client(client_socket: socket.socket, client_addr: Tuple[str, int], buffer_size: int = BUFFER_SIZE) -> None:
    """Handle the client and read the message contained within MSG_START_ID and MSG_END_ID"""
    buffer = b""

    while True:
        packet = client_socket.recv(buffer_size)
        if not packet:
            client_socket.sendall(json.dumps({"status": ERROR}).encode())
            client_socket.close()
            break
        buffer += packet

        # find message frame if present
        msg_start_idx = find_pattern(buffer, MSG_START_ID)[1]
        msg_end_idx = find_pattern(buffer, MSG_END_ID)[1]

        if msg_start_idx == -1 or msg_end_idx == -1:
            continue

        msg_obj = json.loads(buffer[msg_start_idx + len(MSG_START_ID):msg_end_idx])
        print("MSG", msg_obj)
        update_plot(x=msg_obj["x"], y=msg_obj["y"])
        buffer = b""
        client_socket.sendall(json.dumps({"status": OK}).encode())


def run_server(host: str = HOST, port: int = PORT) -> None:
    """Start the server and listen for incoming connections"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    initiate_plot()
    while True:
        # waiting for new clients
        client_socket, client_addr = server_socket.accept()

        # create a function: handle_client(client_socket, client_addr)
        handle_client(client_socket, client_addr)


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
