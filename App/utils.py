import random
import pandas as pd
import streamlit as st
from openai import OpenAI
import json
import openai
import os



def load_data_citations_difficiles(file_path1):
    """
    Charge les données à partir d'un fichier CSV et retourne les données et les personnages uniques.
    """
    data = pd.read_csv(file_path1)
   
    return data 


def generate_quote_question(data, characters):
    # Sélectionner une phrase et la bonne réponse
    question = data.sample(1).iloc[0]
    quote = question['Réplique']
    correct_answer = question['Personnage']

    # Générer des mauvaises options
    wrong_options = characters[characters['Personnage'] != correct_answer].sample(n=3, weights = "Poids")['Personnage'].tolist()
    options = wrong_options + [correct_answer]
    random.shuffle(options)

    # Retourner la question sous forme de dictionnaire
    return {"phrase": quote, "options": options, "correct_answer": correct_answer}




def generate_question_citations_difficiles(data, weights_data):
    # Sélectionner une phrase et la bonne réponse
    question = data.sample(1).iloc[0]
    phrase = question['Réplique']
    correct_answer = question['Personnage']

    # Charger la matrice de similarité
    perso_similaire = pd.read_csv("App/Utils/Characters_Similarity.csv", index_col=0)

    # Vérifier que correct_answer est dans la matrice
    if correct_answer not in perso_similaire.columns:
        raise ValueError(f"Le personnage '{correct_answer}' n'est pas dans la matrice de similarité.")

    # Trouver les 10 personnages les plus similaires
    similar_personnages = (
        perso_similaire[correct_answer]  # Récupérer la colonne des similarités
        .drop(index=correct_answer)      # Exclure le personnage correct
        .nlargest(15)                    # Garder les 10 plus similaires
        .index.tolist()                  # Obtenir leurs noms
    )

    # Filtrer les poids pour ne garder que les personnages similaires
    filtered_weights = weights_data[weights_data['Personnage'].isin(similar_personnages)].copy()

    # Renormaliser les poids pour qu'ils s'additionnent à 1
    filtered_weights['Poids'] /= filtered_weights['Poids'].sum()

    # Sélectionner 3 mauvaises options en utilisant un échantillonnage pondéré
    wrong_options = filtered_weights.sample(n=3, weights='Poids')['Personnage'].tolist()

    # Construire les options
    options = wrong_options + [correct_answer]
    random.shuffle(options)

    # Retourner la question sous forme de dictionnaire
    return {"phrase": phrase, "options": options, "correct_answer": correct_answer}




def generate_all_questions(num_questions, data, perso):
    questions = []
    for _ in range(num_questions):
        questions.append(generate_quote_question(data, perso))
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
    with open(f"App/chunk/{random_chunk}.txt", "r", encoding="utf-8") as file:
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
    "Utilise les mêmes terme que dans le texte lors que tu le peux."
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

def texte_information():
    st.markdown("""

**plongez dans l'univers de Kaamelott et de défiez vos connaissances ?**  

**Voici les deux types de quiz disponible :**

### 1. Les Questions Générales

- **Le concept :**  
Répondez à des questions sur Kaamelott en choisissant la bonne réponse parmi 4 propositions.

- **Particularité :**  
Les questions sont générées par ChatGPT en se basant sur une partie précise du script de la série.  
Il est donc possible que certaines questions portent sur le même épisode dans un même quiz. 
La génération du quiz peut prendre quelques instant, c'est tout à fait normal.

- **Attention aux erreurs :**  
Bien que cela ne devrait pas être fréquent, il peut arriver qu’une réponse soit incorrecte. Si une réponse vous semble étrange, vous pourriez avoir raison : n’hésitez pas à vérifier par vous-même !

---

### 2. Les Citations

- **Le concept :**  
À chaque lancement de quiz, un nombre aléatoire de répliques est sélectionné parmi un immense répertoire de citations cultes de Kaamelott(dépendamment du niveau de difficulté choisi). Votre objectif ? Deviner quel personnage a prononcé chacune d’entre elles.
#### **Les niveaux de difficulté :**
- **Facile :**  
Uniquement les répliques les plus emblématiques.
- **Moyen :**  
Les répliques sont tirées au hasard dans l'entierté du livre 1 à 3.
- **Difficile :**  
Même contenu que le niveau moyen, mais avec un twist :  
Les propositions incluent uniquement des personnages ayant des répliques similaires, rendant le choix plus complexe !

---

**Prêt à relever le défi ? Créez un quiz et replongez dans l’univers extraordinaire de Kaamelott !**
""")
