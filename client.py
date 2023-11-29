import socket
import json
import random
import time

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
MSG_START_ID = b"+++"
MSG_END_ID = b"---"


def generate_coordinates() -> dict:
    x = random.randrange(100)
    y = random.randrange(100)
    return {"x": x, "y": y}


def run_client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    while True:
        coordinates = generate_coordinates()
        json_data = json.dumps(coordinates).encode()
        client_socket.sendall(MSG_START_ID + json_data + MSG_END_ID)
        response = client_socket.recv(BUFFER_SIZE)
        response = json.loads(response)  # why does it accumulate? because buffer was not reset

        if response.get("status") == "ERROR":
            print(response)

        time.sleep(2)
    # client_socket.close()


if __name__ == "__main__":
    run_client()
