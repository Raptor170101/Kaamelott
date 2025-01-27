import streamlit as st
from App.utils import load_css, texte_information

def display_home_page():
    """
    Affiche la page d'accueil de l'application Quiz.
    """
    load_css("App/Style.css")

    st.image("C:/Users/theof/vsc/Kaamelott/App/Utils/Kaamelott.png")

    st.title("Bienvenue sur le Quiz Kaamelott")
    st.write("Choisissez votre style de quiz et définissez vos préférences pour commencer !")


    with st.expander("Informations", expanded=False):
     texte_information()
     
    # Sélection du style de quiz
    st.subheader("Style de quiz")
    quiz_style = st.radio(
        "Sélectionnez le style de quiz :",
        ("Questions générales", "Citations"),
        key="quiz_style"
    )

    if quiz_style == "Citations":
          # Sélection du niveau de difficulté
          st.subheader("Niveau de difficulté")
          difficulty_level = st.radio(
               "Choisissez un niveau de difficulté :",
               ("Facile", "Moyen", "Difficile"),
               key="difficulty_level"
          )

    # Sélection du nombre de questions
    st.subheader("Nombre de questions")
    num_questions = st.number_input(
        "Combien de questions voulez-vous ? (1-20)",
        min_value=1,
        max_value=20,
        value=10,
        step=1,
        key="num_questions"
    )

    # Bouton pour passer à l'étape suivante
    if st.button("Commencer le Quiz", key="test"):
        if st.session_state.get("quiz_style") == "Citations" and st.session_state.get("difficulty_level") == "Moyen":
             st.session_state.current_page = "citations_moyennes"
             st.rerun()
        elif st.session_state.get("quiz_style") == "Citations" and st.session_state.get("difficulty_level") == "Facile":
             st.session_state.current_page = "citations_faciles"
             st.rerun()
        elif st.session_state.get("quiz_style") == "Citations" and st.session_state.get("difficulty_level") == "Difficile":
             st.session_state.current_page = "citations_difficiles"
             st.rerun()
        elif st.session_state.get("quiz_style") == "Questions générales" :
             st.session_state.current_page = "Questions_Générales"
             st.rerun()
        

    


# Vérifiez si le script est directement exécuté
if __name__ == "__main__":
    display_home_page()
