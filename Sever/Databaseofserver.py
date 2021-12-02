
import sqlite3
import threading
import time
from datetime import datetime,timedelta
from fuzzywuzzy import process
from requests import exceptions
from tkinter import messagebox
import os

USER_DATABASE_PATH =  "Server Database\Database.db"


class ServerDatabase:
    def __init__(self):
        self.setup_database()

    """Chuẩn bị cơ sở dữ liệu"""
    def setup_database(self):
        """Kết nối đến database"""
        try:
            with sqlite3.connect(USER_DATABASE_PATH,check_same_thread=False) as conn:
                cursor = conn.cursor()
                
                """Tạo bảng dữ liệu người dùng nếu chưa tồn tại"""
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        userID INTEGER PRIMARY KEY,
                        username VARCHAR(20) NOT NULL,
                        password VARCHAR(20) NOT NULL
                    )           
                """)
                
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error",e)
            os._exit(1)
    
    """Hàm tìm dữ liệu người dùng trong cơ sở dữ liệu"""
    def find_user_info(username):
        with sqlite3.connect(USER_DATABASE_PATH,check_same_thread = False) as conn:
            cursor = conn.cursor()
            find_user = ("SELECT * FROM users WHERE username = ?")
            cursor.execute(find_user,[username])
            result =  cursor.fetchall() 
        
        return result

    """Hàm nhập dữ liệu người dùng vào cơ sở dữ liệu"""
    def insert_user(username,password):
        with sqlite3.connect(USER_DATABASE_PATH,check_same_thread = False) as conn:
            cursor = conn.cursor()
            insert_user = ("""INSERT INTO users (username,password) VALUES (?, ?)""")
            cursor.execute(insert_user,[(username),(password)])
            conn.commit()
            

    """Tìm từ database"""    
    def query_from_database(name,date):
        
        date_format = datetime.strptime(date,"%Y%m%d").strftime("%#d/%#m/%Y")
        if ServerDatabase.check_gold_table_exists(date_format) == False:
            if ServerDatabase.create_table_in_gold_database(date) == False:
                return None
        results =  ServerDatabase.find_approximate_from_database(name,date_format)
        return results
    
    """Kiểm tra xem bảng đã có trong database hay chưa"""
    def check_gold_table_exists(table_name):
        with sqlite3.connect(GOLDS_DATABASE_PATH,check_same_thread = False) as conn:
            cur = conn.cursor()
            find_table = cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name= '{table_name}'""").fetchall()
        if find_table == []:
            return False
        return True
    
    """Lấy list tên vàng từ database"""
    def get_name_of_golds(date = datetime.now()):
        date = date.strftime("%#d/%#m/%Y")
        with sqlite3.connect(GOLDS_DATABASE_PATH,check_same_thread = False) as conn:
            cursor = conn.cursor()   
            list_of_name = cursor.execute(f"SELECT NAME FROM '{date}' ORDER BY rowid").fetchall()
            list_of_name = [name[0] for name in list_of_name]
            return list_of_name 
        
  
               