from utils.utils import *
import streamlit as st
import pandas as pd

# LE TABELLE SONO GIA' STATE CREATE QUINDI PARTI DIRETTA CON LE QUERY
if __name__ == "__main__":
    st.title("🏢 :green[Agenzie]")
    # Crea 3 colonne per salvare la prima query
    col1, col2, col3 = st.columns(3)
    # Controlla la connessione al DB prima di procedere
    if check_connection():
        # Prima query: quante agenzie distinte nel DB?
        # Se fai la group by ti viene un elenco di 1
        query = "SELECT COUNT(*) AS 'numAgenzie' FROM AGENZIA;"
        # Esegue la prima query e la salva in una variabile
        agenzieN = execute_query(st.session_state["connection"], query)
        # Seconda query: Quante città distinte in elenco?
        query = "SELECT COUNT(DISTINCT Citta_Indirizzo) AS numCittà FROM `AGENZIA`;"
        # Esegue la seconda query e la salva in una variabile
        agenzieCity = execute_query(st.session_state["connection"], query)
        # Terza query: Stampa le città con più agenzie in ordine decrescente
        query = "SELECT Citta_Indirizzo, COUNT(*) AS num FROM `AGENZIA` GROUP BY Citta_Indirizzo ORDER BY `num` DESC LIMIT 1;"
        # Esegue la terza query e la salva in una variabile
        city = execute_query(st.session_state["connection"], query)
        # Riempie le colonne precedentemente create con le variabili in cui sono salvate le query
        # colN.metric(NomeCol, valore)
        col1.metric(label = "Numero di Agenzie", value = agenzieN.mappings().first()['numAgenzie'])
        col2.metric(label = "Numero di Città", value = agenzieCity.mappings().first()["numCittà"])
        col3.metric(label = "Città con più agenzie", value = city.mappings().first()["Citta_Indirizzo"])
        # .mappings() non è un metodo standard di streamlit o pandas, restituisce struttura dati iterabile di cui viene preso solo il primo elemento

        # Quarta query: per ogni agenzia viene memorizzato
        query = "SELECT DISTINCT AGENZIA.Citta_Indirizzo, CITTA.Latitudine AS 'LAT', CITTA.Longitudine AS 'LON' FROM `AGENZIA`,CITTA WHERE AGENZIA.Citta_Indirizzo=CITTA.Nome;"
        # Esegue la quarta query e la salva in una variabile del tipo lista di dizionari o dizionario di liste
        citygeo = execute_query(st.session_state["connection"], query)

        # Crea variabile contenente un dataframe(nome, larghezza, lunghezza)
        df_map = pd.DataFrame(citygeo)
        # I dati geografici (città, lat, long) vengono riportati nella mappa
        st.map(df_map)

        # Variabile che stampa su schermo la frase "-" seguita da una riga vuota dedicata a ciò che vuole scrivere l'utente
        cityName = st.text_input("Filtra per città")
        if cityName == '':
            # Se l'utente non scrive nulla prendi tutte le agenzie
            query = "SELECT Citta_Indirizzo, CONCAT(Via_Indirizzo, ' ', Numero_Indirizzo) AS 'Indirizzo' FROM `AGENZIA`;"
        else:
            # Altrimenti prendi solo quelle con la città data in input
            query = f"SELECT Citta_Indirizzo, CONCAT(Via_Indirizzo, ' ', Numero_Indirizzo) AS 'Indirizzo' FROM `AGENZIA` WHERE Citta_Indirizzo='{cityName}'"

        # La 'f' davanti al corpo della query significa che l'espressione tra {} è una stringa formattata di python
        # Per creare il secondo campo della tabella concatenadue attributi della tabella di partenza con CONCAT

        # Esegue la query scritta nell'if
        cityInfo = execute_query(st.session_state["connection"], query)
        # Crea variabile da inserire nel dataframe
        df_info = pd.DataFrame(cityInfo)
        # Genera dataframe = tabella
        st.dataframe(df_info, use_container_width=True)
