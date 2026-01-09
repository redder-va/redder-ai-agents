import sqlite3
from datetime import datetime

class FeedbackHandler:
    def __init__(self, db_path='feedback/feedback.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                agent_name TEXT,
                user_feedback TEXT,
                rating INTEGER,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def store_feedback(self, agent_name, feedback, rating):
        timestamp = datetime.now().isoformat()
        self.conn.execute('''
            INSERT INTO feedback (agent_name, user_feedback, rating, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (agent_name, feedback, rating, timestamp))
        self.conn.commit()

    def get_feedback(self, agent_name=None):
        if agent_name:
            cursor = self.conn.execute('SELECT * FROM feedback WHERE agent_name = ?', (agent_name,))
        else:
            cursor = self.conn.execute('SELECT * FROM feedback')
        return cursor.fetchall()

    def close(self):
        self.conn.close()