# Handles persistent chat memory for the Solvine desktop app using SQLite.
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'chat_memory.db')

class ChatMemory:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS conversation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            ''')

    def add_message(self, sender, message):
        with self.conn:
            self.conn.execute(
                'INSERT INTO conversation (timestamp, sender, message) VALUES (?, ?, ?)',
                (datetime.now().isoformat(), sender, message)
            )

    def get_history(self, limit=100):
        cur = self.conn.cursor()
        cur.execute('SELECT timestamp, sender, message FROM conversation ORDER BY id DESC LIMIT ?', (limit,))
        return cur.fetchall()[::-1]  # Return in chronological order

    def search_messages(self, query, limit=100):
        cur = self.conn.cursor()
        cur.execute('''
            SELECT timestamp, sender, message FROM conversation
            WHERE message LIKE ? OR sender LIKE ?
            ORDER BY id DESC LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        return cur.fetchall()[::-1]

    def close(self):
        self.conn.close()
