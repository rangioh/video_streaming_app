from UI import VideoChatUI
import numpy as np
import cv2
import threading
import tkinter as tk
import socket

class VideochatClient:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 클라이언트")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 2323))

        self.receive_message_thread =threading.Thread(target=self.receive_message)
        self.receive_message_thread.daemon = True
        self.receive_message_thread.start()

    def show_frame(self):

        # 예상 최대 프레임 크기
        received_frame_data = self.client_socket.recv(65536)
        received_frame_array = np.frombuffer(received_frame_data, dtype=np.uint8)
        received_frame = cv2.imdecode(received_frame_array, cv2.IMREAD_COLOR)
        if received_frame is not None:
            self.ui.show_frame(received_frame)

    def send_message_to_server(self, message):
        self.client_socket.send(message.encode())

    def send_message_to_clients(self, message):
        # 클라이언트에서 받은 메세지를 UI에 표시
        self.ui.receive_message(message)

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                # 서버에서 받은 메세지를 UI에 표시
                self.send_message_to_clients(message)
            except:
                pass

if __name__ == "__main__":
    client = VideochatClient()