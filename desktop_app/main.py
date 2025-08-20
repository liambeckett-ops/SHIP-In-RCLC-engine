import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

import threading
import speech_recognition as sr
import pyttsx3
import os
import sys
# Ensure src and its submodules are importable
SRC_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SRC_PARENT not in sys.path:
    sys.path.insert(0, SRC_PARENT)
# from src.core_engine import CognitiveCore


from chat_memory import ChatMemory
import requests

# --- Ollama LLM integration ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def get_agent_response(user_input):
    """Send user input to Ollama and return the LLM's reply."""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": user_input,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[Ollama error: No response]")
    except Exception as e:
        return f"[Ollama error: {e}]"


class ChatWindow(QWidget):
    memory = None
    agent_response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solvine Desktop Assistant")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.tts_engine = pyttsx3.init()
        self.agent_response_signal.connect(self.display_agent_response)
        self.memory = ChatMemory()
        self.load_history()

    def load_history(self):
        history = self.memory.get_history(limit=100)
        for timestamp, sender, message in history:
            self.chat_display.append(f"{sender}: {message}")

    def init_ui(self):
        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        # Search bar
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Search conversation history...")
        self.search_line.returnPressed.connect(self.search_history)
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_history)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_line)
        search_layout.addWidget(search_btn)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type your message or use the mic...")
        self.input_line.returnPressed.connect(self.send_message)
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        mic_btn = QPushButton("🎤")
        mic_btn.clicked.connect(self.voice_input)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(send_btn)
        btn_layout.addWidget(mic_btn)
        layout.addWidget(QLabel("Solvine Assistant"))
        layout.addLayout(search_layout)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_line)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def search_history(self):
        query = self.search_line.text().strip()
        if not query:
            return
        results = self.memory.search_messages(query, limit=100)
        self.chat_display.clear()
        self.chat_display.append(f"Search results for: '{query}'\n")
        if not results:
            self.chat_display.append("No matches found.")
        else:
            for timestamp, sender, message in results:
                self.chat_display.append(f"{sender}: {message}")

    def send_message(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
        self.chat_display.append(f"You: {user_text}")
        self.memory.add_message("You", user_text)
        self.input_line.clear()
        threading.Thread(target=self.handle_agent_response, args=(user_text,)).start()

    def handle_agent_response(self, user_text):
        response = get_agent_response(user_text)
        self.memory.add_message("Solvine", response)
        self.agent_response_signal.emit(response)
        # self.speak(response)  # Temporarily disabled to debug crash

    def display_agent_response(self, response):
        self.chat_display.append(f"Solvine: {response}")

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_display.append("[Listening...]")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            user_text = recognizer.recognize_google(audio)
            self.chat_display.append(f"You (voice): {user_text}")
            self.memory.add_message("You (voice)", user_text)
            threading.Thread(target=self.handle_agent_response, args=(user_text,)).start()
        except Exception as e:
            self.chat_display.append(f"[Voice Error] {e}")

    def speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()