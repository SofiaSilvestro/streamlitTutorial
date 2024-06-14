import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *
import pymysql, cryptography

if __name__ == "__main__":
    st.set_page_config(
        page_title="Quaderno 4",
        layout="wide",
        page_icon="📖",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Corso di *Basi di Dati*"
        }
    )

st.title("💻:blue[Corso di Basi di Dati:] :red[Quaderno 4]📁")
st.markdown("## 🤸🏻:green[Gestione prenotazioni palestra🏋🏻]")
st.markdown("### :blue[Studente:] :violet[*Sofia Silvestro*] 👧🏻")
st.markdown("_In questa applicazione si hanno a disposizione più pagine, ognuna con funzionalità diversa._")

st.text("Di seguito l'istogramma che visualizza il numero di lezioni che cominciano nello stesso orario:")
query = "SELECT COUNT(*) AS N, OraInizio FROM Programma GROUP BY OraInizio;"
Nlez1 = execute_query(st.session_state["connection"], query)
st.bar_chart(data=Nlez1, x='OraInizio', y='N')

#ordine_giorni = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
#df = pd.DataFrame(ordine_giorni)

st.text("Di seguito il diagramma ad area che visualizza il numero di corsi che si svolgono in una stessa giornata:")
query = "SELECT COUNT(*) AS NumLez, Giorno FROM Programma GROUP BY Giorno;"
Nlez2 = execute_query(st.session_state["connection"], query)
st.area_chart(Nlez2, x='Giorno', y='NumLez')



if "connection" not in st.session_state.keys():
    st.session_state["connection"] = False

check_connection()

st.sidebar.image("images/polito.png")

