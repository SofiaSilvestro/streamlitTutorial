import streamlit as st
from utils.utils import *
import pandas as pd

def get_list(attributo, tabella):
    query = f"SELECT DISTINCT {attributo} FROM {tabella}"
    result = execute_query(st.session_state["connection"], query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list
# Funzione che seleziona un attributo senza ripetizioni da una tabella e mette tutti i valori della riga selezionata da un attributo in una lista

def map_optional(optional):
    query = ""
    for element in optional:
        query = query + (f" AND HAS_OPTIONAL.OPTIONAL_Optional='{element}'")
    return query
# Funzione che restituisce l'output della query, cioè l'attributo selezionato con gli optional dati alla funzione


if __name__ == "__main__":

    # Stampa il titolo del file
    st.title("🛎 :blue[Stanze]")
    # Se la connessione è andata a buon fine
    if check_connection():
        # Primo expander
        with st.expander("Filtri", True):
            col1, col2, col3 = st.columns(3)
            # Filtro le stanze per tipo
            tipo = col1.radio("Tipo di stanza", ["Singola", "Doppia", "Tripla", "Tutte"])

            # Scelta delle stanze in base agli optional
            optionalList = get_list("OPTIONAL_Optional", "HAS_OPTIONAL")
            optional = col2.multiselect("Optional:", optionalList)
            # Richiesta la presenza di un particolare spazio
            cucinaFlag = col1.checkbox("Voglio la cucina")

            optionalQuery = map_optional(optional)
            typeQuery = f"AND Type='{tipo.lower()}'" if tipo != 'Tutte' else ''
            # st.write(optionalQuery)
        if cucinaFlag:
            query = f"""SELECT CodS,Piano,Superficie,Type,HAS_OPTIONAL.OPTIONAL_Optional, HAS_SPAZI.SPAZI_Spazi
            FROM `STANZA`, `HAS_OPTIONAL`,`HAS_SPAZI`
            WHERE CodS=HAS_OPTIONAL.STANZA_CodS AND CodS=HAS_SPAZI.STANZA_CodS {typeQuery} {optionalQuery} AND HAS_SPAZI.SPAZI_Spazi='cucina' 
            """
        else:
            query = f"""SELECT CodS,Piano,Superficie,Type,HAS_OPTIONAL.OPTIONAL_Optional
                FROM `STANZA`, `HAS_OPTIONAL`
                WHERE CodS=HAS_OPTIONAL.STANZA_CodS {typeQuery} {optionalQuery}
                """
        result = execute_query(st.session_state["connection"], query)
        df = pd.DataFrame(result)
        st.dataframe(df, use_container_width=True)

        # OPZIONALE
        # Secondo expander
        with st.expander("Stanze"):
            if cucinaFlag:
                query = f"""SELECT DISTINCT CodS,Piano,Type
                FROM `STANZA`, `HAS_OPTIONAL`,`HAS_SPAZI`
                WHERE CodS=HAS_OPTIONAL.STANZA_CodS AND CodS=HAS_SPAZI.STANZA_CodS {typeQuery} {optionalQuery} AND HAS_SPAZI.SPAZI_Spazi='cucina' 
                GROUP BY CodS
                """
            else:
                query = f"""SELECT DISTINCT CodS,Piano,Type
                    FROM `STANZA`, `HAS_OPTIONAL`
                    WHERE CodS=HAS_OPTIONAL.STANZA_CodS {typeQuery} {optionalQuery}
                    GROUP BY CodS
                    LIMIT 5;
                    """
            result = execute_query(st.session_state["connection"], query)
            df = pd.DataFrame(result)
            for index, row in df.iterrows():
                col1, col2 = st.columns(2)
                col1.subheader(f":green[Risultato {index + 1}]")
                col1.text(f"Codice Stanza: {row['CodS']}")
                col1.text(f"Piano: {row['Piano']}")
                col1.text(f"Tipo: {row['Type']}")
                col2.image(f"images/{row['Type']}.png")