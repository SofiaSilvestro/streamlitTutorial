from utils.utils import *
import streamlit as st
import numpy as np
import pandas as pd


if __name__ == "__main__":
    st.set_page_config(
        page_title="Prima APP",
        layout="wide",
        page_icon="📖",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Corso di *Basi di Dati*"
        }
    )

col1, col2 = st.columns([4, 2])
with col1:
    st.title("🏨 :red[Gestione prenotazioni hotel] 🏨")
    st.markdown("## :blue[Corso di Basi di Dati:] :green[Laboratorio 6 Streamlit]")
    st.subheader(":blue[Studente:] :violet[Sofia] 👧🏻")
    # st.markdown("### Studente: :violet[Sofia] 👧🏻") UGUALE A SOPRA
    st.text("")
with col2:
    st.image("images/polito.png")

if "connection" not in st.session_state.keys():
    st.session_state["connection"] = False

check_connection()
