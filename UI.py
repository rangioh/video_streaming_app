import tkinter as tk
from PIL import Image, ImageTk

class VideoChatUI:
    def __init__(self, window, title):
        self.window = window
        self.window.title(title)

        # 웹캠 이미지 라벨
        self.label = tk.Label(window)
        self.label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

        # 스크롤바 있는 채팅창
        self.chat_scrollbar = tk.Scrollbar(window)
        self.chat_scrollbar.grid(row=0, column=2, sticky='ns')

        self.chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=self.chat_scrollbar.set)
        self.chat_text.grid(row=0, column=1, padx=10, sticky="nsew")
        self.chat_scrollbar.config(command=self.chat_text.yview)

        # 메세지 입력 필드
        self.entry = tk.Entry(window)
        self.entry.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        # 메세지 보내기 버튼
        self.send_button = tk.Button(window, text="보내기", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5, sticky="se")

        # 행 및 열 가중치 설정
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=0)
        window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
        window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

    def show_frame(self, frame):
        if frame is not None:
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.config(image=photo)
            self.label.image = photo

    def send_message(self):
        message = self.entry.get()
        if message:
            self.entry.delete(0, 'end')
            self.on_send_message(message)
            self.receive_message("You: " + message)

    def on_send_message(self, message):
        pass

    def receive_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + '\n')
        self.chat_text.config(state=tk.DISABLED)
        # 최신 메세지로 자동 스크롤
        self.chat_text.see(tk.END)