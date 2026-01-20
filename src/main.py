import tkinter as tk
from tkinter import messagebox
import datetime
import os

# --- Logic Functions ---

def save_to_history(entry_text):
    with open("calc_history.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%H:%M")
        file.write(f"[{timestamp}] {entry_text}\n")

def calculate():
    try:
        expression = entry.get()
        # eval() naturally handles % for modulus
        result = eval(expression) 
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        
        save_to_history(f"{expression} = {result}")
        update_history_display()
    except Exception:
        messagebox.showerror("Error", "Invalid Input")
        entry.delete(0, tk.END)

def backspace():
    """Removes the last character in the entry field."""
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def clear_history_file():
    """Deletes the history file and updates display."""
    if os.path.exists("calc_history.txt"):
        os.remove("calc_history.txt")
    update_history_display()

def update_history_display():
    history_text.config(state=tk.NORMAL)
    history_text.delete('1.0', tk.END)
    try:
        with open("calc_history.txt", "r") as file:
            history_text.insert(tk.END, file.read())
    except FileNotFoundError:
        history_text.insert(tk.END, "No history yet.")
    history_text.config(state=tk.DISABLED)

# --- UI Setup ---

root = tk.Tk()
root.title("Advanced Calc")
root.geometry("350x600")

entry = tk.Entry(root, font=("Arial", 22), borderwidth=2, relief="groove", justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky="nsew")

# Updated buttons list: Added % and ⌫ (Backspace)
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '%', '+',
    '⌫', '='
]

row_val = 1
col_val = 0

for button in buttons:
    if button == '=':
        # Span across two columns for the equals button
        btn = tk.Button(root, text=button, width=10, height=2, command=calculate, bg="#4CAF50", fg="white")
        btn.grid(row=row_val, column=col_val, columnspan=2, padx=2, pady=2, sticky="nsew")
        col_val += 1 
    elif button == 'C':
        btn = tk.Button(root, text=button, width=5, height=2, command=lambda: entry.delete(0, tk.END), bg="#f44336", fg="white")
        btn.grid(row=row_val, column=col_val, padx=2, pady=2, sticky="nsew")
    elif button == '⌫':
        btn = tk.Button(root, text=button, width=5, height=2, command=backspace, bg="#ff9800", fg="white")
        btn.grid(row=row_val, column=col_val, padx=2, pady=2, sticky="nsew")
    else:
        btn = tk.Button(root, text=button, width=5, height=2, command=lambda x=button: entry.insert(tk.END, x))
        btn.grid(row=row_val, column=col_val, padx=2, pady=2, sticky="nsew")
    
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# History Section
tk.Label(root, text="History:", font=("Arial", 10, "bold")).grid(row=6, column=0, pady=(10,0))
history_text = tk.Text(root, height=10, width=40, state=tk.DISABLED, bg="#f9f9f9", font=("Courier", 9))
history_text.grid(row=7, column=0, columnspan=4, padx=10, pady=5)

# Clear History Button
clear_btn = tk.Button(root, text="Clear History Log", command=clear_history_file, bg="#9E9E9E", fg="white", font=("Arial", 8))
clear_btn.grid(row=8, column=0, columnspan=4, pady=5)

update_history_display()
root.mainloop()