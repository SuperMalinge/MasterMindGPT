import tkinter as tk

class Logger:
    def __init__(self, chat_output):
        self.chat_output = chat_output

    def log_to_widget(self, message):        
        self.chat_output.insert(tk.END, f"{message}\n")