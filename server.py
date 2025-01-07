from flask import Flask, jsonify, request, render_template
from datetime import datetime
import sqlite3
import random
import time

app = Flask(__name__)

#Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour récupérer une session de quiz (questions selon le thème choisi)
@app.route('/start_quiz', methods=['GET'])
def start_quiz():
    theme = request.args.get('theme', 'Sciences')  # Thème par défaut
    if theme == "Aléatoire":
        theme = random.choice(["Sciences", "Art et Littérature", "Géographie"])  # Choix aléatoire d'un thème
    
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()

    # Récupérer les questions en fonction du thème et du score
    cursor.execute("""
        SELECT id, question, proposition1, proposition2, proposition3, proposition4, reponse_correcte, points
        FROM Questions WHERE theme=? ORDER BY points DESC LIMIT 5
    """, (theme,))
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

    # Ajouter un timestamp pour mesurer la durée du quiz
    start_time = time.time()
    return jsonify({"quiz": quiz_data, "start_time": start_time})

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

    # Comparaison insensible à la casse
    if correct_answer and user_answer.strip().lower() == correct_answer[0].strip().lower():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect", "correct_answer": correct_answer[0]})

# Route pour sauvegarder le score
@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    nom_joueur = data.get("nom_joueur")
    theme = data.get("theme")
    score = data.get("score")
    start_time = float(data.get("start_time"))
    total_time = round(time.time() - start_time, 2)  # Temps total en secondes

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sauvegarde du score et du temps total dans la base de données
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Scores (nom_joueur, theme, score, temps_total, date)
        VALUES (?, ?, ?, ?, ?)
    """, (nom_joueur, theme, score, total_time, date))
    conn.commit()
    conn.close()

    return jsonify({"message": "Score enregistré avec succès", "total_time": total_time})

# Route pour récupérer les scores (affichage par catégorie)
@app.route('/get_scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nom_joueur, theme, score, temps_total, date
        FROM Scores
        ORDER BY score DESC, temps_total ASC, date ASC
    """)
    scores = cursor.fetchall()
    conn.close()
    return jsonify({"scores": scores})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
