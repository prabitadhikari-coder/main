# ------------------ HIGH DPI FIX (VERY TOP) ------------------
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

import tkinter as tk
from tkinter import scrolledtext, ttk
import requests

# ------------------ OLLAMA CONFIG ------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

AVAILABLE_MODELS = [
    "llama3",
    "phi3"
]

# ------------------ AI CHATBOT CLASS ------------------
class UniversalAIChatbot:
    def __init__(self):
        self.model = "llama3"
        self.context = self._base_context()

    def _base_context(self):
        return (
            "You are a universal AI tutor with expert knowledge in all subjects "
            "including science, math, medicine, engineering, history, arts, "
            "law, and technology. Explain clearly and accurately.\n\n"
        )

    def set_model(self, model_name):
        self.model = model_name
        self.context = self._base_context()

    def get_response(self, user_input):
        payload = {
            "model": self.model,
            "prompt": self.context + f"User: {user_input}\nAI:",
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()

        reply = response.json()["response"].strip()
        self.context += f"User: {user_input}\nAI: {reply}\n"
        return reply


# ------------------ GUI FUNCTIONS ------------------
def send_message():
    user_text = user_entry.get().strip()
    if not user_text:
        return

    chat_area.insert(tk.END, f"You: {user_text}\n\n")
    user_entry.delete(0, tk.END)

    try:
        reply = bot.get_response(user_text)
        chat_area.insert(tk.END, f"AI ({bot.model}): {reply}\n\n")
        chat_area.see(tk.END)

    except requests.exceptions.ConnectionError:
        chat_area.insert(
            tk.END,
            "❌ Ollama is not running.\n"
            "Start it using: ollama run llama3\n\n"
        )

    except Exception as e:
        chat_area.insert(tk.END, f"Error: {e}\n\n")


def change_model(event=None):
    selected = model_var.get()
    bot.set_model(selected)
    chat_area.insert(tk.END, f"🔄 Switched model to: {selected}\n\n")
    chat_area.see(tk.END)


# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("🌍 Universal AI Chatbot")
root.geometry("900x620")
root.minsize(860, 580)
root.configure(bg="#0f172a")

# High-resolution internal scaling
root.tk.call("tk", "scaling", 1.35)

bot = UniversalAIChatbot()

# ------------------ STYLE ------------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground="#020617",
    background="#020617",
    foreground="#e5e7eb",
    arrowcolor="#38bdf8",
    borderwidth=0,
    padding=8
)

# ------------------ TOP BAR ------------------
top_frame = tk.Frame(root, bg="#020617", height=60)
top_frame.pack(fill=tk.X, padx=14, pady=(14, 8))

# App title
tk.Label(
    top_frame,
    text="🤖 Universal AI Chatbot",
    font=("Segoe UI Variable", 16, "bold"),
    fg="#38bdf8",
    bg="#020617"
).pack(side=tk.LEFT, padx=12)

# ---- MODEL SELECT PILL ----
model_pill = tk.Frame(
    top_frame,
    bg="#020617",
    highlightbackground="#38bdf8",
    highlightthickness=1,
    bd=0
)
model_pill.pack(side=tk.RIGHT, padx=12, ipady=4)

tk.Label(
    model_pill,
    text="🧠 MODEL",
    font=("Segoe UI Variable", 10, "bold"),
    fg="#94a3b8",
    bg="#020617"
).pack(side=tk.LEFT, padx=(10, 6))

model_var = tk.StringVar(value="llama3")

model_selector = ttk.Combobox(
    model_pill,
    textvariable=model_var,
    values=AVAILABLE_MODELS,
    state="readonly",
    width=12,
    justify="center"
)
model_selector.pack(side=tk.LEFT, padx=(0, 10), pady=4)
model_selector.bind("<<ComboboxSelected>>", change_model)

# ------------------ CHAT AREA ------------------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Consolas", 11),
    bg="#020617",
    fg="#e5e7eb",
    insertbackground="#38bdf8",
    insertwidth=2,
    relief=tk.FLAT,
    padx=12,
    pady=12
)
chat_area.pack(padx=12, pady=8, fill=tk.BOTH, expand=True)

# ------------------ INPUT AREA ------------------
input_frame = tk.Frame(root, bg="#0f172a")
input_frame.pack(fill=tk.X, padx=12, pady=(4, 12))

user_entry = tk.Entry(
    input_frame,
    font=("Segoe UI Variable", 12),
    bg="#020617",
    fg="#e5e7eb",
    insertbackground="#38bdf8",
    insertwidth=2,
    relief=tk.FLAT
)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
user_entry.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(
    input_frame,
    text="🚀 Send",
    font=("Segoe UI Variable", 11, "bold"),
    bg="#38bdf8",
    fg="#020617",
    activebackground="#0ea5e9",
    activeforeground="#020617",
    relief=tk.FLAT,
    padx=18,
    pady=8,
    command=send_message
)
send_btn.pack(side=tk.RIGHT)

# ------------------ START MESSAGE ------------------
chat_area.insert(
    tk.END,
    "🟢 System Online\n"
    "💡 Select a model and start chatting with your offline AI.\n\n"
)

root.mainloop()