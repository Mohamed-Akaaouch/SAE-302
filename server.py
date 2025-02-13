from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import random
import time

app = Flask(__name__)
app.secret_key = "e8b9f3a6798c473fb5cd342a7d0fe874" 

@app.route('/')
def home():
    if 'user_id' in session:  # Vérification de l'existence de la session
        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Users.username, Scores.theme, Scores.score, Scores.temps_total, Scores.date
            FROM Scores
            JOIN Users ON Scores.user_id = Users.id
            ORDER BY CASE 
                WHEN Scores.theme = 'Aléatoire' THEN 0 
                ELSE 1 
            END, Scores.score DESC, Scores.date DESC
        """)
        scores = cursor.fetchall()
        conn.close()

        return render_template('index.html', scores=scores)

    return redirect(url_for('login'))  # Rediriger vers la page de connexion si non connecté

# Route pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Nom d'utilisateur déjà pris. Veuillez en choisir un autre."
    return render_template('register.html')

# Route pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM Users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('home'))  # Rediriger vers la page d'accueil après connexion
        return "Nom d'utilisateur ou mot de passe incorrect."

    return render_template('login.html')

# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Suppression de l'ID utilisateur de la session
    return redirect(url_for('login'))  # Rediriger vers la page de connexion après déconnexion

# Autres routes (inchangées)...


# Route pour récupérer une session de quiz
@app.route('/start_quiz', methods=['GET'])
def start_quiz():
    if 'user_id' not in session:  # Si la session n'existe pas
        return redirect(url_for('login'))  # Rediriger vers la page de connexion

    theme = request.args.get('theme', 'Sciences')
    
    if theme == "Aléatoire":
        theme = random.choice(["Sciences", "Art et Littérature", "Géographie"])

    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()

    # Nous devons récupérer un nombre aléatoire de questions (par exemple, 5 questions) pour le thème choisi
    cursor.execute("""
        SELECT id, question, proposition1, proposition2, proposition3, proposition4, reponse_correcte, points
        FROM Questions WHERE theme=? 
        ORDER BY RANDOM() LIMIT 5
    """, (theme,))
    
    questions = cursor.fetchall()
    conn.close()

    # Formatage des données pour renvoyer un quiz
    quiz_data = [{"id": q[0], "question": q[1], "propositions": [q[2], q[3], q[4], q[5]], "points": q[7]} for q in questions]
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

    if correct_answer and user_answer.strip().lower() == correct_answer[0].strip().lower():
        return jsonify({"result": "correct"})
    return jsonify({"result": "incorrect", "correct_answer": correct_answer[0]})

@app.route('/save_score', methods=['POST'])
def save_score():
    if 'user_id' not in session:  # Si l'utilisateur n'est pas connecté
        return jsonify({"message": "Vous devez être connecté pour enregistrer votre score."}), 401

    data = request.get_json()
    theme = data['theme']  # Récupère le thème envoyé par le client
    score = data['score']
    start_time = data['start_time']
    user_id = session['user_id']  # Récupère l'ID de l'utilisateur connecté

    # Connexion à la base de données
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()

    # Calcul du temps total et arrondi à 2 chiffres après la virgule
    temps_total = round(time.time() - start_time, 2)

    # Enregistrement du score dans la base de données
    try:
        cursor.execute("""
            INSERT INTO Scores (user_id, theme, score, temps_total, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, theme, score, temps_total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()  # Enregistrez les changements dans la base de données

        return jsonify({"message": "Score enregistré avec succès", "total_time": temps_total})

    except sqlite3.Error as e:
        print("Erreur lors de l'enregistrement du score:", e)
        return jsonify({"message": "Erreur lors de l'enregistrement du score."}), 500

    finally:
        conn.close()  # Fermez la connexion après avoir exécuté la requête


@app.route('/get_scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Users.username, Scores.theme, Scores.score, Scores.temps_total, Scores.date
        FROM Scores
        JOIN Users ON Scores.user_id = Users.id
        ORDER BY CASE 
            WHEN Scores.theme = 'Aléatoire' THEN 0 
            ELSE 1 
        END, Scores.score DESC, Scores.date DESC
    """)
    scores = cursor.fetchall()
    conn.close()

    # Retourne les scores dans le format JSON
    return jsonify({"scores": scores})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
