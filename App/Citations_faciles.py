import streamlit as st
import random
from App.utils import generate_question_citations, load_data_citations_faciles, load_css

def display_citations_faciles():
    """
    Affiche la logique du quiz pour le type Citations et le niveau Moyen.
    """
    load_css("C:/Users/theof/vsc/Kaamelott/App/Style.css")
   
    st.image("C:/Users/theof/vsc/Kaamelott/App/Utils/Kaamelott.png")

    data, perso = load_data_citations_faciles("App/Utils/Citation_faciles.csv", "App/Utils/Personnages_pondéré_faciles.csv")

    # Initialisation des variables dans st.session_state
    if  "questions" not in st.session_state :
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = [
            generate_question_citations(data, perso) for _ in range(num_questions)
            ]
            st.session_state.current_question_index = 0
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
            st.session_state.score = 0
            st.session_state.results = []


    if st.session_state.questions == []:
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = [
            generate_question_citations(data, perso) for _ in range(num_questions)
            ]

  

    # Si le quiz n'est pas terminé
    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.current_question_index]

        # Afficher la phrase
        st.subheader(f"Question {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}")
        st.text_area("", current_question["phrase"], disabled=True, key="citations_faciles")

        # Afficher les options
        selected_option = st.radio("Choisissez le personnage :", current_question["options"])

        # Bouton pour valider la réponse
        if st.button("Répondre"):
            if selected_option:
                # Vérifier la réponse
                if selected_option == current_question["correct_answer"]:
                    st.session_state.feedback = "Bonne réponse ! 🎉"
                    st.session_state.score += 1
                    st.session_state.results.append(
                        {"question": current_question["phrase"], "status": "Correct"}
                    )
                else:
                    st.session_state.feedback = f"Faux ! La bonne réponse était : {current_question['correct_answer']}."
                    st.session_state.results.append(
                        {"question": current_question["phrase"], "status": "Incorrect"}
                    )
                st.session_state.show_feedback = True
            else:
                st.warning("Veuillez sélectionner une option avant de valider.")

        # Afficher le feedback uniquement après validation
        if st.session_state.show_feedback:
            st.text_area("", st.session_state.feedback, disabled=True, key="reponses_citations_faciles")

        # Bouton pour passer à la question suivante
        if st.session_state.show_feedback and st.button("Question suivante"):
            st.session_state.current_question_index += 1
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
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
    display_citations_faciles()
