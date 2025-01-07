import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('quiz_game.db')
cursor = conn.cursor()

# Supprimer toutes les entrées de la table Scores
cursor.execute("DELETE FROM Scores")

# Commit les changements et fermer la connexion
conn.commit()
conn.close()

print("Tous les scores ont été réinitialisés.")
