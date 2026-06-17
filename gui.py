import tkinter as tk
from tkinter import scrolledtext
import time

from chatbot import (
    load_knowledge,
    process_message
)

knowledge = load_knowledge()
start_time = time.time()


# -------------------------
# SEND MESSAGE
# -------------------------

def send_message():

    user_message = user_entry.get()

    if not user_message.strip():
        return

    chat_area.config(state=tk.NORMAL)

    chat_area.insert(tk.END, f"\nYou: {user_message}\n")

    bot_response = process_message(
        user_message,
        knowledge,
        start_time
    )

    chat_area.insert(tk.END, f"Bot: {bot_response}\n")

    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

    user_entry.delete(0, tk.END)


# -------------------------
# WINDOW
# -------------------------

root = tk.Tk()
root.title("Smart AI Chatbot Assistant")
root.geometry("700x600")
root.resizable(False, False)

# -------------------------
# TITLE
# -------------------------

title = tk.Label(
    root,
    text="SMART AI CHATBOT ASSISTANT",
    font=("Arial", 16, "bold")
)

title.pack(pady=10)

# -------------------------
# CHAT AREA
# -------------------------

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=75,
    height=25,
    state=tk.DISABLED
)

chat_area.pack(padx=10, pady=10)

# -------------------------
# INPUT FRAME
# -------------------------

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10)

user_entry = tk.Entry(
    input_frame,
    font=("Arial", 12)
)

user_entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    padx=(0, 10)
)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message
)

send_button.pack(side=tk.RIGHT)

root.mainloop()