import random
import pandas as pd
import streamlit as st
from openai import OpenAI
import json
import openai
import os


def load_data_citations_faciles(file_path1, file_path2):
    """
    Charge les données à partir d'un fichier CSV et retourne les données et les personnages uniques.
    """
    data = pd.read_csv(file_path1)
    perso = pd.read_csv(file_path2)
    return data, perso


def load_data_citations_moyennes_difficiles(file_path1, file_path2):
    """
    Charge les données à partir d'un fichier CSV et retourne les données et les personnages uniques.
    """
    data = pd.read_csv(file_path1)
    perso = pd.read_csv(file_path2)
    return data, perso


def load_data_citations_difficiles(file_path1):
    """
    Charge les données à partir d'un fichier CSV et retourne les données et les personnages uniques.
    """
    data = pd.read_csv(file_path1)
   
    return data 


def generate_question_citations(data, perso):
    # Sélectionner une phrase et la bonne réponse
    question = data.sample(1).iloc[0]
    phrase = question['Réplique']
    correct_answer = question['Personnage']

    # Générer des mauvaises options
    wrong_options = perso[perso['Personnage'] != correct_answer].sample(n=3, weights = "Poids")['Personnage'].tolist()
    options = wrong_options + [correct_answer]
    random.shuffle(options)

    # Retourner la question sous forme de dictionnaire
    return {"phrase": phrase, "options": options, "correct_answer": correct_answer}


def generate_question_citations_difficiles(data):
    # Sélectionner une phrase et la bonne réponse
    question = data.sample(1).iloc[0]
    phrase = question['Réplique']
    correct_answer = question['Personnage']

    # Charger la matrice de similarité
    perso_similaire = pd.read_csv("App/Utils/Similarité_entre_Personnages.csv", index_col=0)

    # Vérifier que correct_answer est dans la matrice
    if correct_answer not in perso_similaire.columns:
        raise ValueError(f"Le personnage '{correct_answer}' n'est pas dans la matrice de similarité.")

    # Trouver les 10 personnages les plus similaires
    similar_personnages = (
        perso_similaire[correct_answer]  # Récupérer la colonne des similarités
        .drop(index=correct_answer)      # Exclure le personnage correct
        .nlargest(10)                    # Garder les 10 plus similaires
        .index.tolist()                  # Obtenir leurs noms
    )

    # Sélectionner 3 mauvaises options parmi ces personnages similaires
    wrong_options = random.sample(similar_personnages, 3)

    # Ajouter la bonne réponse et mélanger
    options = wrong_options + [correct_answer]
    random.shuffle(options)

    # Retourner la question sous forme de dictionnaire
    return {"phrase": phrase, "options": options, "correct_answer": correct_answer}


def generate_all_questions(num_questions, data, perso):
    questions = []
    for _ in range(num_questions):
        questions.append(generate_question_citations(data, perso))
    return questions


def generate_all_questions_difficiles(num_questions, data, perso):
    questions = []
    for _ in range(num_questions):
        questions.append(generate_question_citations_difficiles(data, perso))
    return questions


def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")


def create_questions_Générales(num_questions):


    api_key = os.getenv("KAAMELOTT_API")

    openai.api_key = api_key

    random_chunk = random.randint(1, 101)
    with open(f"C:/Users/theof/vsc/Kaamelott/App/chunk/{random_chunk}.txt", "r", encoding="utf-8") as file:
        file_content = file.read()


    themes = ["absurde", "heroisme", "politique", "relations humaines", "amour", "réflexion"]

    selected_themes = random.choices(themes, k=num_questions)

    prompt = (
    f"Le texte ci-dessous est extrait d'un fichier qui constitue la seule source d'information pour cette tâche. "
    "Avant de commencer anaylse l'entierté du document"
    f"Crée {num_questions} questions de quiz sur Kaamelott, chacune basée sur un thème que je vais te fournir. "
    f"Les thèmes à utiliser sont : {', '.join(selected_themes)}.\n\n"
    "sois particulièrement attentif à ce que les questions que tu créer soient intéressantes pour un fan de Kaamelott\n"
    "Il faut donc que les questions portent sur des chose remarquables de l'histoire ou des détails intéressants"
    "Donne du contexte aux questions si tu juges que qu'il est nécessaire pour pouvoir répondre correctement"
    "Donne toujours le nom de l'épisode auquel la question fait référence et essai d'avoir le moins de questions possibles portant sur le même épisode"
    "Fait également attention à ce qu'il n'y ai qu'une seule réponse correct"
    "La réponse correcte doit être d'une exactitude sans faille"
    "Il faut que le quiz soit de niveau moyen, une personne qui connaît bien Kaamelott doit pouvoir répondre sans problème mais une personne qui le connaît peu doit être incertain des réponses"
    f"Renvoie les résultats dans un format JSON avec la structure suivante :\n"
    "["
    "  {"
    "    \"question\": \"Texte de la question\","
    "    \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],"
    "    \"correct_answer\": \"Texte de la bonne réponse\""
    "  },"
    "  ..."
    "]\n\n"
    "Voici un exemple concret :\n"
    "["
    "  {"
    "    \"question\": \"Quel est l'élément central autour duquel Arthur souhaite réunir les Chevaliers de Bretagne ?\","
    "    \"options\": [\"Une épée légendaire\", \"La Table Ronde\", \"Un trône en or\", \"Un bouclier magique\"],"
    "    \"correct_answer\": \"La Table Ronde\""
    "  },"
    "  {"
    "    \"question\": \"Quel personnage s'efforce de faire des tartes pour ses futurs petits-enfants ?\","
    "    \"options\": [\"Guenièvre\", \"La Dame du Lac\", \"Séli\", \"Angharad\"],"
    "    \"correct_answer\": \"Séli\""
    "  }"
    "]\n\n"
    "Ne renvoie que les réponses avec le format demandé et aucun autre commentaire.\n\n"
    f"Voici le contenu du fichier :\n{file_content}\n\n"
    "Attention : tu ne dois pas utiliser de connaissances externes au texte fourni pour répondre à cette demande."
    )
    



    # Appeler l'API
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    question = completion.choices[0].message.content

    if question.startswith("```json"):
        question = question[7:]  # Supprime "```json" au début
    if question.endswith("```"):
        question = question[:-3]

    # Conversion de la chaîne JSON en une liste Python

    question = json.loads(question)  # Transforme la chaîne JSON en liste de dictionnaires
    
    return question


