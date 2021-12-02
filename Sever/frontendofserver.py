
import re
import socket
import threading
import tkinter as tk
import time
import os
from Constofserver import ICON

"""Hàm căn giữa màn hình"""
def center(master,app_width,app_height):
    SCREEN_HEIGHT = master.winfo_screenheight()
    SCREEN_WIDTH = master.winfo_screenwidth()
    
    x = (SCREEN_WIDTH/2) - (app_width/2)  
    y = (SCREEN_HEIGHT/2) - (app_height/2)
    
    master.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")   


"""Trang chính của chương trình"""                        
class MainPage:
    def __init__(self,master):
        self.root = master
        self.root.title("SERVER")
        self.root.iconbitmap(f"{ICON}")
        self.disconnect_flag = False
        
        """Kích thước của app"""
        self.app_height = 400
        self.app_width = 700

        center(self.root,self.app_width,self.app_height)

        self.messages_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.status_list = tk.Listbox(self.messages_frame,width = 100,height = 22,yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.status_list.pack()

        self.messages_frame.pack()

        self.quit_but = tk.Button(self.root,text = "Quit",width = 30,command = self.on_closing)
        self.quit_but.pack(pady = (10,10))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    """Set cờ khi server muốn dừng kết nối"""
    def set_disconnect_flag(self,bool):
        self.disconnect_flag = bool
    
    """Hàm để lấy cái cờ ngắt kết nối ra khỏi đối tượng"""
    def get_disconnect_flag(self):
        return self.disconnect_flag
    
    """Hàm nhập vào ô text box hiện thông tin"""
    def insert_to_text_box(self,msg):
        self.status_list.insert(tk.END,msg)
    
    """Hàm khi tắt server"""
    def on_closing(self):
        self.set_disconnect_flag(True)  
        
  