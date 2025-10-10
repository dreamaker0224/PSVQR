import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
import keyboard  # 用於監聽熱鍵

clicking = False

def clicker(interval):
    global clicking
    while clicking:
        pyautogui.click()
        time.sleep(interval / 1000)  # 毫秒轉秒

def start_clicking():
    global clicking
    if clicking:
        return
    try:
        interval = float(interval_entry.get())
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字！")
        return
    clicking = True
    status_label.config(text="狀態：連點中", fg="green")
    t = threading.Thread(target=clicker, args=(interval,))
    t.daemon = True
    t.start()

def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="狀態：停止", fg="red")

def toggle_clicking():
    if clicking:
        stop_clicking()
    else:
        start_clicking()

def hotkey_listener():
    keyboard.add_hotkey("esc", toggle_clicking)  # ESC 切換啟動/停止
    keyboard.wait()  # 保持監聽

# GUI 建立
root = tk.Tk()
root.title("滑鼠連點器")

tk.Label(root, text="連點間隔（毫秒）：").pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.pack(pady=5)
interval_entry.insert(0, "100")  # 預設 100ms

start_button = tk.Button(root, text="開始連點", command=start_clicking, width=20, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="停止連點", command=stop_clicking, width=20, bg="red", fg="white")
stop_button.pack(pady=5)

status_label = tk.Label(root, text="狀態：停止", fg="red")
status_label.pack(pady=5)

# 啟動熱鍵監聽
t = threading.Thread(target=hotkey_listener)
t.daemon = True
t.start()

root.mainloop()
