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


# TODO: data type for message param in send_reponse
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


def get_response_message(status: str, message: str) -> bytes:
    """Prepare a JSON response to the client regarding packet status"""
    for elem in (status, message):
        if not isinstance(elem, str):
            raise TypeError("status and message must be of type str")

    response = {"status": status, "message": message}
    serialized_response = json.dumps(response).encode()
    return serialized_response
    # client_socket.sendall(serialized_response)  # todo move client socket from this function


def handle_client(client_socket: socket.socket, client_addr: Union[str, int], buffer_size: int = BUFFER_SIZE) -> None:
    """Handle the client and read the message contained within MSG_START_ID and MSG_END_ID markers"""
    buffer = b""

    while True:
        packet = client_socket.recv(buffer_size)

        # analyze packet -> new_buffer,

        if not packet:
            error_message = "socket connection is closed or there is an error"
            response = get_response_message(ERROR, error_message)
            client_socket.sendall(response)
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
            response = get_response_message(ERROR, f"{e.__class__.__name__}: {e}")
            client_socket.sendall(response)
            buffer = b""
            continue

        x = msg_obj.get("x")
        y = msg_obj.get("y")

        # TODO consider to make a func
        if None in (x, y):
            error_message = str()
            if not x and not y:
                error_message = "missing x and y values"
            elif not x and y:
                error_message = "missing x value"
            elif not y and x:
                error_message = "missing y value"
            response = get_response_message(ERROR, error_message)
            client_socket.sendall(response)
            buffer = b""
            continue

        update_plot(x=x, y=y)
        response = get_response_message(OK, "coordinates received")
        client_socket.sendall(response)
        buffer = b""


def run_server(host: str = HOST, port: int = PORT) -> None:
    """Start the server and listen for incoming connections"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    initiate_plot()
    while True:
        # waiting for new clients
        client_socket, client_addr = server_socket.accept()

        handle_client(client_socket, client_addr)


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
