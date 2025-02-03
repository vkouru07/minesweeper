import sqlite3
import json
from hashlib import sha256

'''
To avoid uneccessary operations, only a max of 5 highscores are stored at any given moment. 
'''

# Connect to the SQLite database (or create it if it doesn't exist)
def init_database (): 
    global conn, cursor 
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()

    # Create a table to store high scores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS highscores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        signature TEXT NOT NULL
    )
    ''')
    conn.commit()

def save_high_score(player_name, score):
    # Create a dictionary to store the high score data
    high_score = {
        'player_name': player_name,
        'score': score
    }

    # Serialize the data to JSON
    high_score_json = json.dumps(high_score).encode('utf-8')

    # Generate a SHA256 hash of the high score data
    signature = sha256(high_score_json).hexdigest()

    # Load the top five high scores from the database
    cursor.execute('SELECT * FROM highscores ORDER BY score DESC LIMIT 5')
    top_five_high_scores = cursor.fetchall()

    # Check if the new score is higher than any of the top five high scores
    for high_score in top_five_high_scores:
        if high_score[2] <= score:
            # If it is, update the corresponding high score in the database
            cursor.execute('''
            UPDATE highscores
            SET score = ?, signature = ?
            WHERE player_name = ?
            ''', (score, sha256(high_score_json).hexdigest(), player_name))

            # Commit the changes and break the loop
            conn.commit()
            break
    else:
        # If the new score is not higher than any of the top five high scores,
        # do not insert it into the database
        print("Score not high enough to be a top score.")

    # Commit the changes if a high score was updated
    conn.commit()


def load_high_scores():
    # Query the high scores from the database
    cursor.execute('SELECT * FROM highscores ORDER BY score DESC LIMIT 5')
    high_scores = cursor.fetchall()

    # Deserialize the high score data and verify the signatures
    loaded_high_scores = []
    for row in high_scores:
        high_score_json = row[1].encode('utf-8')
        signature = row[2]

        calculated_signature = sha256(high_score_json).hexdigest()

        if signature == calculated_signature:
            high_score = json.loads(high_score_json.decode('utf-8'))
            loaded_high_scores.append(high_score)

    return loaded_high_scores

# def update_top_five(player_name, score):
#     # Load all high scores from the database
#     all_high_scores = load_high_scores()

#     # Update the player's score if necessary 
#     for i, high_score in enumerate(all_high_scores):
#         if high_score['player_name'] == player_name:
#             all_high_scores[i]['score'] = score
#             break

#     # Sort the high scores in descending order
#     all_high_scores.sort(key=lambda x: x['score'], reverse=True)

#     # Limit to the top five high scores
#     all_high_scores = all_high_scores[:5]

#     # Update the database with the top five high scores
#     for high_score in all_high_scores:
#         cursor.execute('''
#         UPDATE highscores
#         SET score = ?, signature = ?
#         WHERE player_name = ?
#         ''', (high_score['score'], sha256(json.dumps(high_score).encode('utf-8')).hexdigest(), high_score['player_name']))

#     conn.commit()