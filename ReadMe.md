# Kaamelott Quiz

## Description du projet

Kaamelott Quiz est une application permettant de générer des quiz illimités sur l'univers de **Kaamelott**. Deux types de quiz sont disponibles :

1. **Quiz sur les citations** : le joueur doit retrouver quel personnage a prononcé une réplique.
2. **Quiz de questions générales** : le joueur répond à des questions sur l'univers de la série.

Essayez l'application ici : [Kaamelott Quiz](https://kaamelott-quiz.streamlit.app/)

---

## Fonctionnement du projet

### 🎭 Quiz basé sur les citations

Ces quiz sont générés à partir de fichiers CSV contenant des paires **citation/personnage**. Pour chaque question, une citation est sélectionnée au hasard, et trois autres personnages sont proposés comme fausses réponses.

Trois niveaux de difficulté sont disponibles :

- **Facile** :
  - Les citations proviennent d'une base restreinte contenant uniquement les plus connues.
  - Les mauvaises réponses sont choisies aléatoirement dans la liste des personnages, en excluant celui qui a dit la réplique.

- **Moyen** :
  - Toutes les citations du script des trois premiers Livres de Kaamelott sont utilisées.
  - Les mauvaises réponses sont sélectionnées en tenant compte du **poids** de chaque personnage (nombre de citations du personnage / nombre total de citations).
  - Cette approche limite l'apparition de personnages très secondaires dans les choix de réponse, évitant ainsi des éliminations trop faciles.

- **Difficile** :
  - Même principe que le niveau moyen, mais les mauvaises réponses sont sélectionnées parmi les **15 personnages les plus similaires** à celui ayant dit la réplique.
  - La similarité est calculée à l’aide de **cosine_similarity**, appliquée sur l’ensemble des répliques des personnages.

---

### ❓ Quiz de questions générales

Les questions sont générées dynamiquement via l'API **GPT-4o** :

1. Un extrait du script de Kaamelott est sélectionné aléatoirement parmi 100 morceaux pré-découpés (pour limiter le nombre de tokens envoyés).
2. Cet extrait est utilisé comme contexte pour formuler une requête à l’API.
3. L’API retourne une question et ses réponses au format **JSON**.
4. Ces données sont transformées en dictionnaire Python pour être utilisées dans l’application.

---

## 🛠 Technologies utilisées

- **Streamlit** :
  - Simplicité de création et de déploiement de l'application.
  - Apprentissage de l’outil dans le cadre du projet.
- **Python** : gestion des données et de la logique du quiz.
- **Pandas** : manipulation des fichiers CSV.
- **Scikit-learn** : calcul de la similarité entre personnages.
- **API GPT-4o** : génération des questions générales.

---

## Logique du code 

Voici la liste des fichiers importants pour la logique du code et leur utilité :
**Utils.py** : Contient les fonctions principales utilisée dans les autres fichier
**Home.py** : Contient le code de la page d'acceuil
**Easy_Quotes.py** : Contient le code de la page du quiz des citations en mode facil
**Medium_Quotes.py** : Contient le code de la page du quiz des citations en mode moyen
**Hard_Quotes.py** : Contient le code de la page du quiz des citations en mode difficil
**General_Questions.py** Contient le code de la page du quiz des questions générales

---
## 🚀 Installation et exécution

### Prérequis
- Python 3.8+
- Un environnement virtuel recommandé (`venv` ou `conda`)

### Installation
```bash
# Cloner le dépôt
git clone https://github.com/ton_repo/kaamelott-quiz.git
cd kaamelott-quiz

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

#API GPT
Si vous voulez utiliser le code en local, il vous faudra ajouter votre clé API de GPT-4o dans une variable d'environnement nommé "KAAMELOTT_API"
```

### Exécution
```bash
streamlit run app.py
```

---

## 📌 Améliorations possibles

- Ajouter un mode **multijoueur** pour comparer les scores en temps réel.
- Permettre aux utilisateurs de **soumettre leurs propres citations**.
- Intégrer un système de **badges et récompenses** pour encourager la progression.
- Étendre la base de données avec **les Livres suivants** de Kaamelott.

---

Si vous avez des suggestions ou souhaitez contribuer, n’hésitez pas à ouvrir une issue ou un pull request sur le dépôt GitHub ! 🔥

