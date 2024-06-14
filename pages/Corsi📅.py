from utils.utils import *
import streamlit as st
import pandas as pd

if __name__ == "__main__":
    st.title("🤸🏻 :green[CORSI] 📅")
    col1, col2 = st.columns(2)
    if check_connection():
        query = "SELECT COUNT(*) AS 'NumeroCorsi' FROM Corsi;"
        NCorsi = execute_query(st.session_state["connection"], query)

        query = "SELECT COUNT(*) AS NumTipi FROM (SELECT COUNT(*) AS Parziale FROM Corsi GROUP BY Tipo) AS NT;"
        NTipi = execute_query(st.session_state["connection"], query)

        col1.metric(label="Numero di corsi", value=NCorsi.mappings().first()['NumeroCorsi'])
        col2.metric(label="Numero di tipi distinti di corsi", value=NTipi.mappings().first()['NumTipi'])

        st.subheader(":blue[Scegliere il corso]")

        query = "SELECT DISTINCT Nome FROM `Corsi`;"
        ElencoCorsi = execute_query(st.session_state["connection"], query)
        ElencoCorsi = [corso[0] for corso in ElencoCorsi]
        NomeCorsoScelto = st.selectbox("Scegli il nome del corso", ElencoCorsi)

        query = "SELECT DISTINCT Tipo FROM `Corsi`;"
        ElencoTipi = execute_query(st.session_state["connection"], query)
        ElencoTipi = [tipo[0] for tipo in ElencoTipi]
        TipoCorsoScelto = st.selectbox("Scegli il tipo del corso", ElencoTipi)

        query = "SELECT DISTINCT Livello FROM `Corsi` ORDER BY Livello;"
        ElencoLivelli = execute_query(st.session_state["connection"], query)
        ElencoLivelli = [livello[0] for livello in ElencoLivelli]
        LivelloCorsoScelto = st.selectbox("Scegli il livello del corso", ElencoLivelli)

        query = f"SELECT CodC FROM `Corsi` WHERE Nome = '{NomeCorsoScelto}' AND Tipo = '{TipoCorsoScelto}' AND Livello = '{LivelloCorsoScelto}'"
        CodiceScelto = execute_query(st.session_state["connection"], query)
        CodiceScelto = [Codice[0] for Codice in CodiceScelto]

        if CodiceScelto:
            query = f"SELECT P.CodC, I.Nome, I.Cognome, P.Giorno, P.OraInizio, P.Durata, P.Sala FROM Istruttore I, Corsi C, Programma P WHERE I.CodFisc = P.CodFisc AND C.CodC = P.CodC AND C.Nome = '{NomeCorsoScelto}' AND C.Tipo = '{TipoCorsoScelto}' AND C.Livello = '{LivelloCorsoScelto}'"
            InfoCorso = execute_query(st.session_state["connection"], query)
            df_info = pd.DataFrame(InfoCorso)
            st.dataframe(df_info, use_container_width=True)
        else:
            st.error("Corso inesistente!")


