from utils.utils import *
import streamlit as st
import pandas as pd
from datetime import date, time

def get_list(attributo):
    query = f"SELECT DISTINCT {attributo} FROM Programma"
    result = execute_query(st.session_state["connection"],query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list

def get_info():
    return get_list("CodFisc"), get_list("Giorno"), get_list("CodC"), get_list("Sala")

def check_info(lezdict):
    for value in lezdict.values():
        if value == '':
            return False
    return True

# inserisce il nuova lezione
def insert(Lezione):
    if check_info(Lezione):
        attributi = ", ".join(Lezione.keys())
        valori = tuple(Lezione.values())
        query = f"INSERT INTO Programma ({attributi}) VALUES {valori};"
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False
def create_form():
    with st.form("Nuova Lezione Programmata"):
        st.subheader("🏋🏻Informazioni Nuova Lezione💃🏻")
        query = "SELECT CodFisc FROM `Istruttore`;"
        ElencoIstruttori = execute_query(st.session_state["connection"], query)
        ElencoIstruttori = [istr[0] for istr in ElencoIstruttori]
        codfisc = st.selectbox("Scegli l'istruttore del corso", ElencoIstruttori)

        giorno = st.text_input("Giorno della settimana", placeholder="Giorno scelto")

        orainizio = st.slider("Orario di inizio", min_value=time(9, 0), max_value=time(18, 0))
        st.write("La lezione inizia alle: ", orainizio)
        orainizio = str(orainizio)

        durata = st.slider("Durata della lezione", min_value=15, max_value=60, step=5)
        st.write("La lezione dura: ", durata)

        query = "SELECT Nome FROM Corsi;"
        ElencoCorsi = execute_query(st.session_state["connection"], query)
        ElencoCorsi = [corso[0] for corso in ElencoCorsi]
        nomecorso = st.selectbox("Scegli il nome della lezione a cui partecipare", ElencoCorsi)
        query = f"SELECT CodC FROM Corsi WHERE Nome = '{nomecorso}'"
        codicecorso = execute_query(st.session_state["connection"], query)
        codicecorso = [codc[0] for codc in codicecorso]

        query = "SELECT DISTINCT Sala FROM `Programma` ORDER BY Sala;"
        ElencoSale = execute_query(st.session_state["connection"], query)
        ElencoSale = [sala[0] for sala in ElencoSale]
        sala = st.selectbox("Scegli la sala della lezione", ElencoSale)

        insert_dict = {"CodFisc": codfisc, "Giorno": giorno, "OraInizio": orainizio, "Durata": durata, "CodC": codicecorso[0], "Sala": sala}

        submitted = st.form_submit_button("Salva la nuova lezione")

        query = f"SELECT CodC FROM `Programma` WHERE CodC <> '{codicecorso[0]}' AND Giorno <> '{giorno}'"
        verifica = execute_query(st.session_state["connection"], query)
        verifica = [ver[0] for ver in verifica]

    if submitted:
        #if codicecorso[0] in verifica:
            if giorno != 'Sabato' and giorno != 'Domenica':
                if insert(insert_dict):
                    st.success("Lezione inserita correttamente")
                    st.write(insert_dict)
                else:
                    st.error("Inserimento fallito")
            else:
                st.error("Inserimento fallito: giorno non valido")
        #else:
            #st.error("Inserimento fallito: lezione già presente in questa giornata")

if __name__ == "__main__":
    st.title("🚲 :green[INSERIRE NUOVA LEZIONE]🎈")
    if check_connection():
        create_form()
