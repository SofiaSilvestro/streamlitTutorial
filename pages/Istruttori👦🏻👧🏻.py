# Problemi con il formato delle date

from utils.utils import *

import datetime
import streamlit as st
import pandas as pd
#from datetime import date

def get_list(attributo):
    query=f"SELECT {attributo} FROM Istruttore"
    result=execute_query(st.session_state["connection"],query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list

if __name__ == "__main__":
    st.title("🏃🏻 :blue[ISTRUTTORI] 🚴🏻")
    col1, col2 = st.columns(2)
    if check_connection():
        Istruttore = st.text_input(label="Scrivere il cognome dell'istruttore scelto:", value="", max_chars=30)

        DateSel = st.date_input(label="Scegli range di date:", value=(datetime.date(1980, 12, 31), datetime.date(1996, 8, 5)), min_value=datetime.date(1980, 12, 31), max_value=datetime.date(1996, 8, 5))

        ListaIstruttori = get_list("Cognome")

        if Istruttore == '':
            query = "SELECT CodFisc, Nome, Cognome, DataNascita FROM Istruttore"
            Scelta = execute_query(st.session_state["connection"], query)

            df = pd.DataFrame(Scelta)
            for index, row in df.iterrows():
                col1, col2 = st.columns(2)
                col1.subheader(f":red[Istruttore]")
                col1.text(f"Nome: {row['Nome']}")
                col1.text(f"Cognome: {row['Cognome']}")
                col1.text(f"DataNascita: {row['DataNascita']}")
                col1.text(f"CodFisc: {row['CodFisc']}")
                col2.image(f"images/{row['CodFisc']}.png")

        elif Istruttore != '':
            query = f"SELECT CodFisc, Nome, Cognome, DataNascita FROM Istruttore WHERE Cognome = '{Istruttore}' AND DataNascita <= '1996/08/05' AND DataNascita >= '1980/12/31'"
            Scelta = execute_query(st.session_state["connection"], query)

            if Scelta == '':
                st.error("Istruttore non disponibile")
            else:
                df = pd.DataFrame(Scelta)
                for index, row in df.iterrows():
                    col1, col2 = st.columns(2)
                    col1.subheader(f":red[Istruttore]")
                    col1.text(f"Nome: {row['Nome']}")
                    col1.text(f"Cognome: {row['Cognome']}")
                    col1.text(f"DataNascita: {row['DataNascita']}")
                    col1.text(f"CodFisc: {row['CodFisc']}")
                    col2.image(f"images/{row['CodFisc']}.png")

