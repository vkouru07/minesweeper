import sqlite3

class HighScoreManager:
    def __init__(self, db_name='highscores.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection and initialize the cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._initialize_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the database connection
        if self.conn:
            self.conn.close()

    def _initialize_db(self):
        # Create the highscores table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_score(self, player_name, score):
        # Fetch the current top 5 scores
        self.cursor.execute('SELECT score FROM highscores ORDER BY score DESC LIMIT 5')
        top_scores = self.cursor.fetchall()

        # If there are less than 5 scores or the new score is higher than the lowest top score
        if len(top_scores) < 5 or score > top_scores[-1][0]:
            # Insert the new score
            self.cursor.execute('INSERT INTO highscores (player_name, score) VALUES (?, ?)', (player_name, score))
            self.conn.commit()

            # If there are now more than 5 scores, delete the lowest score
            self.cursor.execute('SELECT id FROM highscores ORDER BY score DESC LIMIT 5 OFFSET 5')
            ids_to_delete = self.cursor.fetchall()
            for id_to_delete in ids_to_delete:
                self.cursor.execute('DELETE FROM highscores WHERE id = ?', (id_to_delete[0],))
            self.conn.commit()
            return True  # New high score
        return False  # Not a high score

    def get_highscores(self):
        # Fetch and return the top 5 scores
        self.cursor.execute('SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT 5')
        return self.cursor.fetchall()