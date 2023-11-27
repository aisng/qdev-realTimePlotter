import socket
import json
import matplotlib.pyplot as plt
import numpy as np

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1
MSG_START_ID = b"+++"
MSG_END_ID = b"---"
OK = "OK"
ERROR = "ERROR"


def handle_packets(packets, x_vals, y_vals):
    current_coordinates = json.loads(packets.pop(0))
    x_vals.append(current_coordinates["x"])
    y_vals.append(current_coordinates["y"])
    return x_vals, y_vals


def update_line(hl, new_data):
    hl.set_xdata(np.append(hl.get_xdata(), new_data))
    hl.set_ydata(np.append(hl.get_ydata(), new_data))
    plt.draw()


def handle_client(client_socket, client_addr):
    client_messages = []
    buffer = b""
    is_buffering = False
    # msg_frame = {"start_symbols": 0, "end_symbols": 0}

    while True:
        packet = client_socket.recv(BUFFER_SIZE)
        if not packet:
            client_socket.sendall(json.dumps({"status": ERROR}).encode())
            client_socket.close()
            break

        # waiting for start idx
        if packet in MSG_START_ID and not is_buffering:
            buffer += packet
            if buffer.startswith(MSG_START_ID):
                is_buffering = True
            continue
            # msg_frame["start_symbols"] += 1

        if is_buffering:
            buffer += packet

        if buffer.endswith(MSG_END_ID):
            buffer = buffer.lstrip(MSG_START_ID)
            buffer = buffer.rstrip(MSG_END_ID)
            msg_obj = json.loads(buffer)
            print(msg_obj)
            # call function to update plot(x,y)
            # make buffer size reading as parameter

            buffer = b""
            is_buffering = False

        # if packet in MSG_END_ID:
        #     msg_frame["end_symbols"] += 1
        #
        # if msg_frame["end_symbols"] == len(MSG_END_ID):
        #     is_buffering = False
        #     msg_frame["end_symbols"] = 0
        #
        # if is_buffering:
        #     print("packet when found", packet)
        #     buffer += packet
        #     print(buffer)
        #     if MSG_END_ID in buffer:
        #         client_messages.append(buffer.split(MSG_END_ID)[0])
        #
        # if msg_frame["start_symbols"] == len(MSG_START_ID):
        #     is_buffering = True
        #     msg_frame["start_symbols"] = 0

        # print(client_messages)
        # this currently works if packets are of size 1
        # if packet not in MSG_START_ID and packet not in MSG_END_ID:
        #     buffer += packet
        # else:
        #     if buffer:
        #         client_messages.append(buffer)
        #     buffer = b""

        # print("buffer", buffer)
        # print("client_messages", client_messages)
        client_socket.sendall(json.dumps({"status": OK}).encode())


def run_server(host=HOST, port=PORT, buffer_size=BUFFER_SIZE, msg_start_id=MSG_START_ID):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        # waiting for new clients
        client_socket, client_addr = server_socket.accept()

        # create a function: handle_client(client_socket, client_addr)
        handle_client(client_socket, client_addr)


def main():
    run_server()


if __name__ == "__main__":
    main()
