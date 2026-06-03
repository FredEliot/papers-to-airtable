import streamlit as st
from dotenv import load_dotenv
from pappers_utils import rechercher_entreprise
import os

st.set_page_config(page_title="Recherche entreprise", page_icon="🏢")  # ⬅️ tout en haut

# Chargement des variables d'environnement
load_dotenv("config/.env")

st.title("🔎 Recherche d'entreprise")

nom = st.text_input("Nom de l'entreprise")

if st.button("Rechercher"):
    resultats = rechercher_entreprise(nom)
    if not resultats:
        st.warning("Aucun résultat trouvé.")
    else:
        st.success(f"{len(resultats)} résultat(s) trouvé(s)")

        for r in resultats:
            with st.expander(f"📌 {r['nom_entreprise']} – SIREN {r['siren']}"):
                st.markdown(f"""
                **Forme juridique** : {r.get('forme_juridique', 'N/A')}  
                **Activité** : {r.get('activite', 'N/A')}  
                **Adresse** : {r.get('siege', 'N/A')}  
                **Dirigeant principal** : {r.get('dirigeant', 'N/A')}
                """)

