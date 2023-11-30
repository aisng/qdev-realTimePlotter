import socket
import json
import matplotlib.pyplot as plt
from typing import Tuple, Union

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

    plt.plot(x, y, "bo", linewidth=2, markersize=4)
    plt.pause(0.1)


def find_pattern(data: Union[str, bytes], pattern: Union[str, bytes]) -> Tuple[bool, int]:
    """Find an element or a pattern in a string or bytestring object"""
    for elem in (data, pattern):
        if not isinstance(elem, (str, bytes)):
            raise TypeError("data and pattern must be of type str or bytes")

    if not isinstance(data, type(pattern)):
        raise TypeError("data and pattern must be of the same type")

    if len(data) < len(pattern):
        return False, -1

    for i in range(len(data) - len(pattern) + 1):
        if data[i:i + len(pattern)] == pattern:
            return True, i
    return False, -1


# TODO: find the right message type, cause now on success a dict is passed
def send_response(client_socket: socket.socket, status: str, message: str) -> None:
    """Send a JSON  response to the client"""
    for elem in (status, message):
        if not isinstance(elem, str):
            raise TypeError("status and message must be of type str")

    response = {"status": status, "message": message}
    serialized_response = json.dumps(response).encode()
    client_socket.sendall(serialized_response)


def handle_client(client_socket: socket.socket, client_addr: Union[str, int], buffer_size: int = BUFFER_SIZE) -> None:
    """Handle the client and read the message contained within MSG_START_ID and MSG_END_ID"""
    buffer = b""

    while True:
        packet = client_socket.recv(buffer_size)
        if not packet:
            error_message = "packet not received"
            # client_socket.sendall(json.dumps({"status": ERROR, "message": "packet not received"}).encode())
            send_response(client_socket, ERROR, error_message)
            client_socket.close()
            break
        buffer += packet

        # find message frame if present
        result_start, msg_start_idx = find_pattern(buffer, MSG_START_ID)
        result_end, msg_end_idx = find_pattern(buffer, MSG_END_ID)

        if not all([result_start, result_end]):
            continue

        msg_bytes = buffer[msg_start_idx + len(MSG_START_ID):msg_end_idx]
        try:
            msg_obj = json.loads(msg_bytes)
        except json.decoder.JSONDecodeError as e:
            send_response(client_socket, ERROR, f"{e}")

            # client_socket.sendall(json.dumps(
            #     {"status": ERROR, "message": e}).encode())
            buffer = b""
            continue

        x = msg_obj.get("x")
        y = msg_obj.get("y")

        if None in (x, y):
            error_message = str()
            if x is None:
                error_message = "x must be of type int, got None"
            if y is None:
                error_message = "y must be of type int, got None"
            send_response(client_socket, ERROR, error_message)
            buffer = b""
            continue

        print("MSG", msg_obj)
        update_plot(x=x, y=y)
        buffer = b""
        send_response(client_socket, OK, "coordinates received")

        # client_socket.sendall(json.dumps({"status": OK, "message": msg_obj}).encode())


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
