from utils.utils import *
import streamlit as st
import pandas as pd
from datetime import date

def get_list(attributo):
    query = f"SELECT DISTINCT {attributo} FROM Istruttore"
    result = execute_query(st.session_state["connection"],query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list

def get_info():
    return get_list("Nome"), get_list("Cognome")

def check_info(prod_dict):
    for value in prod_dict.values():
        if value == '':
            return False
    return True

# inserisce il nuovo istruttore
def insert(istruttore):
    if check_info(istruttore):
        attributi = ", ".join(istruttore.keys())
        valori = tuple(istruttore.values())
        query = f"INSERT INTO Istruttore ({attributi}) VALUES {valori};"
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
    with st.form("Nuovo Istruttore"):
        st.subheader("Inserimento dati istruttore")
        codfisc = st.text_input("Codice Fiscale", placeholder="LLLLLLLNNLNNLNNNL")
        nome = st.text_input("Nome", placeholder="Nome")
        cognome = st.text_input("Cognome", placeholder="Cognome")
        datanascita = st.text_input("Data di Nascita", value=date.today())
        mail = st.text_input("Indirizzo e-mail", placeholder="E-MAIL")

        telefono = st.radio("Vuoi inserire il numero di telefono?", ['SI', 'NO'])
        if telefono == 'SI':
            telefono = st.text_input("Numero di telefono", placeholder="TELEFONO")
        else:
            telefono = 'NULL'

        insert_dict = {"CodFisc": codfisc, "Nome": nome, "Cognome": cognome, "DataNascita": datanascita, "Email": mail, "Telefono": telefono}

        submitted = st.form_submit_button("Salva i dati inseriti")

    if submitted:
        if insert(insert_dict):
            st.success("Istruttore inserito correttamente")
            st.write(insert_dict)
        else:
            st.error("Inserimento fallito")

if __name__ == "__main__":
    st.title("⛷️ :green[INSERIMENTO ISTRUTTORE] 🏊🏻")
    if check_connection():
        create_form()
