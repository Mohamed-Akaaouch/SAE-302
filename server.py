from flask import Flask, jsonify, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour récupérer une session de quiz (5 questions)
@app.route('/start_quiz', methods=['GET'])
def start_quiz():
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, proposition1, proposition2, proposition3, proposition4, reponse_correcte, points FROM Questions ORDER BY RANDOM() LIMIT 5")
    questions = cursor.fetchall()
    conn.close()
    quiz_data = []
    for question in questions:
        quiz_data.append({
            "id": question[0],
            "question": question[1],
            "propositions": [question[2], question[3], question[4], question[5]],
            "points": question[7]
        })
    return jsonify({"quiz": quiz_data})

# Route pour vérifier une réponse
@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get("id")
    user_answer = data.get("answer")

    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT reponse_correcte FROM Questions WHERE id=?", (question_id,))
    correct_answer = cursor.fetchone()
    conn.close()

    if correct_answer and user_answer.lower() == correct_answer[0].lower():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect", "correct_answer": correct_answer[0]})

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    nom_joueur = data.get("nom_joueur")
    theme = data.get("theme")
    score = data.get("score")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sauvegarde du score dans la base de données
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Scores (nom_joueur, theme, score, date)
        VALUES (?, ?, ?, ?)
    """, (nom_joueur, theme, score, date))
    conn.commit()
    conn.close()

    return jsonify({"message": "Score enregistré avec succès"})

@app.route('/get_scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nom_joueur, theme, score, date FROM Scores ORDER BY score DESC, date ASC")
    scores = cursor.fetchall()
    conn.close()
    return jsonify({"scores": scores})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)