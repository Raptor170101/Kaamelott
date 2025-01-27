import streamlit as st
from App.utils import create_questions_Générales, load_css

def display_questions_générales () :

    load_css("App/Style.css")

    if  "questions" not in st.session_state :
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = create_questions_Générales(num_questions)
            st.session_state.current_question_index = 0
            st.session_state.feedback = ""
            st.session_state.show_feedback = False
            st.session_state.score = 0
            st.session_state.results = []


    if st.session_state.questions == []:
            num_questions = st.session_state.get("num_questions", 10)  # Récupérer le nombre de questions
            st.session_state.questions = create_questions_Générales(num_questions)


    st.image("C:/Users/theof/vsc/Kaamelott/App/Utils/Kaamelott.png")
    
    st.session_state.finish = False

    if st.session_state.current_question_index >= len(st.session_state.questions):
        st.session_state.finish = True
    # Si le quiz n'est pas terminé
    if st.session_state.finish == False :
        current_question = st.session_state.questions[st.session_state.current_question_index]

        # Afficher la phrase
        st.subheader(f"Question {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}")
        st.text_area("Question", current_question["question"], disabled=True, label_visibility="hidden", key = "questions_generales")

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
                            {"question": current_question["question"], "status": "Correct"}
                        )
                        st.session_state.show_feedback = True
                        st.rerun()
                    else:
                        st.session_state.feedback = f"Faux ! La bonne réponse était : {current_question['correct_answer']}."
                        st.session_state.results.append(
                            {"question": current_question["question"], "status": "Incorrect"}
                        )
                    st.session_state.show_feedback = True
                    st.rerun()
                else:
                    st.warning("Veuillez sélectionner une option avant de valider.")

        # Afficher le feedback uniquement après validation
        if st.session_state.show_feedback:
            st.text_area("Réponse", st.session_state.feedback, disabled=True, label_visibility="hidden", key = "reponses_questions_generales")

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
            st.session_state.finish = False
            st.rerun()
    

