import tkinter as tk
from tkinter import scrolledtext
import threading
import subprocess
import os

# Start the monitoring script
def start_monitoring():
    log_box.insert(tk.END, "Starting MiniGuard AI...\n")
    log_box.see(tk.END)

    # Run miniguard.py in a new thread
    def run_script():
        process = subprocess.Popen(['python', 'MiniGuardAI.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            log_box.insert(tk.END, line)
            log_box.see(tk.END)
        log_box.insert(tk.END, "MiniGuard AI stopped.\n")
    
    thread = threading.Thread(target=run_script)
    thread.start()

# Stop script by killing Python process
def stop_monitoring():
    os.system("taskkill /f /im python.exe")
    log_box.insert(tk.END, "Stopped MiniGuard AI.\n")
    log_box.see(tk.END)

# Create GUI window
window = tk.Tk()
window.title("MiniGuard AI - FYP GUI")
window.geometry("600x400")
window.configure(bg="#f2f2f2")

# Title Label
title_label = tk.Label(window, text="MiniGuard AI", font=("Arial", 20, "bold"), bg="#f2f2f2", fg="#333")
title_label.pack(pady=10)

# Start Button
start_btn = tk.Button(window, text="Start Monitoring", command=start_monitoring, font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
start_btn.pack(pady=10)

# Stop Button
stop_btn = tk.Button(window, text="Stop Monitoring", command=stop_monitoring, font=("Arial", 12), bg="#f44336", fg="white", padx=20, pady=5)
stop_btn.pack(pady=5)

# Log box for output
log_box = scrolledtext.ScrolledText(window, width=70, height=15, font=("Consolas", 10))
log_box.pack(pady=10)

# Run the app
window.mainloop()