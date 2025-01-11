import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("quiz_game.db")
cursor = conn.cursor()

# Questions avec un thème combiné Art et Littérature
questions = [
    # Questions à 1 point (20 questions avec 2 propositions)
    ("Sciences", "2 propositions", "L'eau gèle à quelle température ?", "0", "0", "100", None, None, 1),
    ("Sciences", "2 propositions", "Le Soleil est-il une étoile ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "L'Australie est-elle un continent ?", "Oui", "Oui", "Non", None, None, 1),
    ("Art et Littérature", "2 propositions", "Vincent Van Gogh a peint 'La Nuit étoilée' ?", "Oui", "Oui", "Non", None, None, 1),
    ("Sciences", "2 propositions", "Les humains respirent-ils de l'oxygène ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "La capitale de la France est Paris ?", "Oui", "Oui", "Non", None, None, 1),
    ("Art et Littérature", "2 propositions", "La Joconde est exposée au Louvre ?", "Oui", "Oui", "Non", None, None, 1),
    ("Sciences", "2 propositions", "Les plantes produisent-elles de l'oxygène ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "Le Nil traverse l'Égypte ?", "Oui", "Oui", "Non", None, None, 1),
    ("Sciences", "2 propositions", "L'éclair est un phénomène électrique ?", "Oui", "Oui", "Non", None, None, 1),
    ("Art et Littérature", "2 propositions", "Picasso était peintre ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "L'Everest est la montagne la plus haute ?", "Oui", "Oui", "Non", None, None, 1),
    ("Sciences", "2 propositions", "L'eau salée est-elle potable ?", "Non", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "Tokyo est la capitale du Japon ?", "Oui", "Oui", "Non", None, None, 1),
    ("Art et Littérature", "2 propositions", "Léonard de Vinci a peint La Joconde ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "L'Afrique est-elle un continent ?", "Oui", "Oui", "Non", None, None, 1),
    ("Art et Littérature", "2 propositions", "Salvador Dalí était un peintre surréaliste ?", "Oui", "Oui", "Non", None, None, 1),
    ("Sciences", "2 propositions", "La lumière voyage plus vite que le son ?", "Oui", "Oui", "Non", None, None, 1),
    ("Géographie", "2 propositions", "La Russie est le plus grand pays au monde ?", "Oui", "Oui", "Non", None, None, 1),

    # Questions à 3 points (10 questions avec 4 propositions)
    ("Géographie", "4 propositions", "Quelle est la plus grande mer ?", "Mer Méditerranée", "Mer Rouge", "Mer Méditerranée", "Mer Noire", "Mer des Caraïbes", 3),
    ("Art et Littérature", "4 propositions", "Quel peintre a créé 'Les Nénuphars' ?", "Monet", "Van Gogh", "Picasso", "Monet", "Cézanne", 3),
    ("Sciences", "4 propositions", "Quelle est la formule chimique de l'eau ?", "H2O", "O2", "H2", "H2O", "CO2", 3),
    ("Géographie", "4 propositions", "Quelle est la capitale de l'Italie ?", "Rome", "Milan", "Rome", "Venise", "Florence", 3),
    ("Sciences", "4 propositions", "Quelle est l'unité de mesure de la force ?", "Newton", "Pascal", "Joule", "Newton", "Watt", 3),
    ("Art et Littérature", "4 propositions", "Quel artiste a créé 'Le Penseur' ?", "Rodin", "Picasso", "Rodin", "Michel-Ange", "Monet", 3),
    ("Sciences", "4 propositions", "Quel est le plus grand organe du corps humain ?", "La peau", "Le foie", "Les poumons", "La peau", "Le cœur", 3),
    ("Géographie", "4 propositions", "Quelle est la plus longue rivière du monde ?", "Nil", "Amazone", "Nil", "Yang-Tsé", "Mississippi", 3),
    ("Art et Littérature", "4 propositions", "Quel mouvement artistique est associé à Van Gogh ?", "Impressionnisme", "Surréalisme", "Impressionnisme", "Cubisme", "Expressionnisme", 3),
    ("Sciences", "4 propositions", "Quelle planète est connue comme la planète rouge ?", "Mars", "Mars", "Jupiter", "Saturne", "Vénus", 3),

    # Questions à 5 points (5 questions sans propositions)
    ("Sciences", "Sans proposition", "Quelle est la vitesse de la lumière en km/s ?", "300000", None, None, None, None, 5),
    ("Art et Littérature", "Sans proposition", "Qui a peint 'Guernica' ?", "Picasso", None, None, None, None, 5),
    ("Géographie", "Sans proposition", "Quelle chaîne de montagnes traverse le Népal ?", "Himalaya", None, None, None, None, 5),
    ("Sciences", "Sans proposition", "Quelle particule subatomique porte une charge négative ?", "Électron", None, None, None, None, 5),
    ("Art et Littérature", "Sans proposition", "Quel architecte a conçu la tour Eiffel ?", "Gustave Eiffel", None, None, None, None, 5)
]

# Requête d'insertion
cursor.executemany("""
    INSERT INTO Questions (theme, type, question, reponse_correcte, proposition1, proposition2, proposition3, proposition4, points)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", questions)

# Validation et fermeture de la connexion
conn.commit()
conn.close()

print("Ajout de questions avec succès dans la table 'Questions'.")
