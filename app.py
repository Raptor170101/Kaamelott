import streamlit as st
from App.Home import display_home_page
from App.Medium_Quotes import display_citations_moyennes
from App.Easy_Quotes import display_citations_faciles
from App.Hard_Quotes import display_citations_difficiles
from App.General_Questions import display_questions_générales



st.set_page_config(page_icon=":sword:", page_title="Kaamelott Quiz")

# Initialisation de la page actuelle
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


# Navigation entre les pages
if st.session_state.current_page == "home":
    display_home_page()
    
elif st.session_state.current_page == "citations_moyennes":
    display_citations_moyennes()

elif st.session_state.current_page == "citations_faciles":
    display_citations_faciles()

elif st.session_state.current_page == "citations_difficiles":
    display_citations_difficiles()

elif st.session_state.current_page == "Questions_Générales":
    display_questions_générales()


