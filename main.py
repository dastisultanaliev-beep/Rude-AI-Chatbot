
import customtkinter as ctk
from openai import OpenAI

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://bothub.chat/api/v2/openai/v1"
MODEL = "gemini-3.1-flash-lite"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

history = [
    {
        "role": "system",
        "content": "You are a very hostile assistant. You help users, but you do it in a very rude and aggressive way."
    }
]


def add_text(text):
    chat_box.configure(state="normal")
    chat_box.insert("end", text + "\n\n")
    chat_box.configure(state="disabled")
    chat_box.see("end")


def send_message(event=None):
    question = entry.get().strip()

    if not question:
        return

    add_text(f"You: {question}")
    entry.delete(0, "end")

    send_button.configure(text="Wait a moment...")
    app.update()

    history.append({
        "role": "user",
        "content": question
    })

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history
        )

        answer = response.choices[0].message.content

        history.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as err:
        answer = f"Error: {err}"

    add_text(f"AI: {answer}")
    send_button.configure(text="Send")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Chatbot")
app.geometry("600x500")

chat_box = ctk.CTkTextbox(
    app,
    wrap="word",
    font=("Arial", 14)
)
chat_box.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

bottom = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
bottom.pack(
    padx=10,
    pady=(0, 10),
    fill="x"
)

entry = ctk.CTkEntry(
    bottom,
    placeholder_text="Write a message...",
    font=("Arial", 14)
)
entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)

entry.bind("<Return>", send_message)

send_button = ctk.CTkButton(
    bottom,
    text="Send",
    command=send_message
)
send_button.pack(side="right")

add_text("Hey! Hurry up and ask your question!")

app.mainloop()
