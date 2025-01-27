import streamlit as st
import random
import pandas as pd
from App.utils import generate_question_citations_difficiles_test, load_data_citations_difficiles, load_css

def display_citations_difficiles():
    """
    Affiche la logique du quiz pour le type Citations et le niveau Moyen.
    """

    load_css("App/Style.css")
   
    st.image("App/Utils/Kaamelott.png")
    
    data = load_data_citations_difficiles("App/Utils/Kaamelott_Repliques_Livres1_à_3.csv")
    info_poids = pd.read_csv("App/Utils/Personnages_pondéré_moyen.csv")

    # Initialisation des variables dans st.session_state
    if  "questions" not in st.session_state :
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = [
            generate_question_citations_difficiles_test(data, info_poids) for _ in range(num_questions)
            ]
            st.session_state.current_question_index = 0
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
            st.session_state.score = 0
            st.session_state.results = []


    if st.session_state.questions == []:
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = [
            generate_question_citations_difficiles_test(data) for _ in range(num_questions)
            ]

   

    # Si le quiz n'est pas terminé
    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.current_question_index]

        # Afficher la phrase
        st.subheader(f"Question {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}")
        st.text_area("Citation", current_question["phrase"], disabled=True, label_visibility="hidden", key="citations_difficiles")

        # Afficher les options
        selected_option = st.radio("Choisissez le personnage :", current_question["options"])

        if "bouton_repondre" not in st.session_state :
            st.session_state.bouton_repondre = True
        
        # Bouton pour valider la réponse
        if st.session_state.bouton_repondre == True :
            if st.button("Répondre"):
                if selected_option:
                    st.session_state.bouton_repondre = False
                    # Vérifier la réponse
                    if selected_option == current_question["correct_answer"]:
                        st.session_state.feedback = "Bonne réponse ! 🎉"
                        st.session_state.score += 1
                        st.session_state.results.append(
                            {"question": current_question["phrase"], "status": "Correct"}
                        )
                        st.session_state.show_feedback = True
                        st.rerun
                    else:
                        st.session_state.feedback = f"Faux ! La bonne réponse était : {current_question['correct_answer']}."
                        st.session_state.results.append(
                            {"question": current_question["phrase"], "status": "Incorrect"}
                        )
                    st.session_state.show_feedback = True
                    st.rerun()
                else:
                    st.warning("Veuillez sélectionner une option avant de valider.")

        # Afficher le feedback uniquement après validation
        if st.session_state.show_feedback:
            st.text_area("Réponse", st.session_state.feedback, disabled=True, label_visibility="hidden", key="reponses_citations_difficiles")

        # Bouton pour passer à la question suivante
        if st.session_state.show_feedback and st.button("Question suivante"):
            st.session_state.current_question_index += 1
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
            st.session_state.bouton_repondre = True
            st.rerun()
    else:
        # Affichage des résultats finaux
        st.success("Quiz terminé !")
        st.write(f"Votre score final est de : {st.session_state.score}/{len(st.session_state.questions)}")
    

        # Bouton pour recommencer
        if st.button("Retour au menu"):
            st.session_state.questions = []
            st.session_state.current_question_index = 0
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
            st.session_state.score = 0
            st.session_state.results = []
            st.session_state.current_page = "home"
            st.rerun()

# Vérifiez si le script est directement exécuté
if __name__ == "__main__":
    display_citations_difficiles()
