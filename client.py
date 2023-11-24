import socket
import json
import random
import time

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
IDENTIFIER = b"+++"


def generate_coordinates():
    x = random.randrange(100)
    y = random.randrange(100)
    return {"x": x, "y": y}


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        coordinates = generate_coordinates()

        json_data = json.dumps(coordinates).encode()
        s.sendall(IDENTIFIER + json_data)
        response = s.recv(BUFFER_SIZE).decode()
        print(f"{response=}")
        time.sleep(2)


if __name__ == "__main__":
    main()
