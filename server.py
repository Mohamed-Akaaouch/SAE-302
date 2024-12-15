from flask import Flask, jsonify, request, render_template
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)