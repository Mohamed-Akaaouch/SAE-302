import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("quiz_game.db")
cursor = conn.cursor()

# Insertion de questions 
questions = [
    ("Sciences", "2 propositions", "Quelle est la planète la plus proche du Soleil ?", "Mercure", "Mercure", "Vénus", None, None, 1),
    ("Géographie", "4 propositions", "Quel est le plus grand continent ?", "Asie", "Afrique", "Amérique", "Antarctique", "Asie", 3),
    ("Art", "Sans proposition", "Qui a peint la Joconde ?", "Léonard de Vinci", None, None, None, None, 5),
    ("Sciences", "2 propositions", "L'eau bout à 100 degrés Celsius ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "4 propositions", "Quel est le plus long fleuve du monde ?", "Nil", "Nil", "Amazone", "Yang-Tsé", "Mississippi", 3)
]

# Requête d'insertion
cursor.executemany("""
INSERT INTO Questions (theme, type, question, reponse_correcte, proposition1, proposition2, proposition3, proposition4, points)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", questions)

# Validation et fermeture de la connexion
conn.commit()
conn.close()

print("Questions ajoutées avec succès.")
