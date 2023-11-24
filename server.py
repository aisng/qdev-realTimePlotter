import socket
import json

HOST = "127.0.0.1"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data_bytes = conn.recv(1024)
                if not data_bytes:
                    break
                data_json = json.loads(data_bytes)
                print(data_json)
                conn.sendall(data_bytes)
