from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)

# Fonction pour récupérer une question aléatoire depuis la base de données
def get_random_question():
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, proposition1, proposition2, proposition3, proposition4, reponse_correcte, points FROM Questions ORDER BY RANDOM() LIMIT 1")
    question = cursor.fetchone()
    conn.close()
    return question

# Route pour récupérer une question
@app.route('/get_question', methods=['GET'])
def get_question():
    question = get_random_question()
    if question:
        question_data = {
            "id": question[0],
            "question": question[1],
            "propositions": [question[2], question[3], question[4], question[5]],
            "points": question[7]
        }
        return jsonify(question_data)
    return jsonify({"error": "Aucune question trouvée"}), 404

# Route pour vérifier la réponse
@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get("id")
    user_answer = data.get("answer")
    
    # Vérification de la réponse dans la base de données
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT reponse_correcte FROM Questions WHERE id=?", (question_id,))
    correct_answer = cursor.fetchone()
    conn.close()
    
    if correct_answer and user_answer.lower() == correct_answer[0].lower():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect", "correct_answer": correct_answer[0]})

if __name__ == '__main__':
    app.run(debug=True)
