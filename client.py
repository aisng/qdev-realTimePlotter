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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        coordinates = generate_coordinates()
        json_data = json.dumps(coordinates).encode()
        s.sendall(MSG_START_ID + json_data + MSG_END_ID)
        response = s.recv(BUFFER_SIZE).decode()
        print(f"{response}")
        time.sleep(2)


if __name__ == "__main__":
    run_client()
