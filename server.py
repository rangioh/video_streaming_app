import cv2
import socket
import threading
from UI import VideoChatUI
import tkinter as tk

class VideochatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 2323))
        self.server_socket.listen(5)

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        # 핸들러에 괄호 넣으면 안됨, 자동생성 주의
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()


        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)


    def send_message_to_clients(self, message):
        for client in self.client:
            client.send(message.encode())
        # 서버 UI에도 메세지 표시
        self.ui.receive_message("서버: " + message)

    def send_message_to_server(self, message):
        # 서버에서 받은 메세지를 UI에 표시
        self.ui.receive_message(message)
        # 받은 메세지를 다른 클라이언트에게도 전송

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            encoded_frame = encoded_frame.tobytes()

            # 오류 데이터 저장
            client_to_remove = []
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    client_to_remove.append(client)

            for client in client_to_remove:
                self.clients.remove(client)

            # 서버 UI에도 비디오 화면 표시
            self.show_frame(frame)

    # 클라이언트 연결 유지
    def receive_clients(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            self.clients.append(client_socket)

            self.socket_thread = threading.Thread(target=self.send_message_to_server)
            self.socket_thread.daemon = True
            self.socket_thread.start()

            self.socket_thread = threading.Thread(target=self.send_message_to_clients)
            self.socket_thread.daemon = True
            self.socket_thread.start()

if __name__ == "__main__":
    server = VideochatServer()
