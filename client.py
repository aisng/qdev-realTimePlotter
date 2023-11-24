import socket
import json
import random
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def generate_coordinates():
    x = random.randrange(10)
    y = random.randrange(10)
    return {"x": x, "y": y}


while True:
    coordinates = generate_coordinates()

    json_data = json.dumps(coordinates).encode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json_data)

        data = s.recv(1024)

    print(f"Received {data}")

    time.sleep(2)
