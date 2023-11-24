import socket
import json
import matplotlib.pyplot as plt

HOST = "127.0.0.1"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1
IDENTIFIER = b"+++"


def main():
    response_ok = {"status": "ok"}
    response_error = {"status": "error"}
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = b""
                packets = []
                while True:
                    packet = conn.recv(BUFFER_SIZE)
                    if not packet:
                        conn.sendall(json.dumps(response_error).encode())
                        break
                    data += packet
                    if IDENTIFIER in data:
                        current_packet = data.split(IDENTIFIER)[0]
                        # print("LEN", len(current_packet))
                        if len(current_packet) > 0:
                            packets.append(current_packet)

                        data = b""
                        print(packets)

                    # print(json.loads(packets.pop(0)))
                    conn.sendall(json.dumps(response_ok).encode())


if __name__ == "__main__":
    main()
