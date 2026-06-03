import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Chargement du fichier .env
load_dotenv(dotenv_path=Path("config") / ".env")

BASE_URL = "https://api.pappers.fr/v2"

def rechercher_entreprise(identifiant):
    api_key = os.getenv("PAPPERS_API_KEY")

    if not api_key:
        raise ValueError("Clé API Pappers introuvable. Vérifie ton fichier .env.")

    if not identifiant:
        return []

    # Requête de recherche initiale
    params = {
        "api_token": api_key,
        "q": identifiant,
        "par_page": 5
    }

    recherche_response = requests.get(f"{BASE_URL}/recherche", params=params)

    if recherche_response.status_code != 200:
        print(f"Erreur API recherche : {recherche_response.status_code}")
        return []

    entreprises = recherche_response.json().get("resultats", [])
    resultats = []

    for e in entreprises:
        siren = e.get("siren")
        if not siren:
            continue

        # Requête détaillée par siren
        details_response = requests.get(
            f"{BASE_URL}/entreprise",
            params={"api_token": api_key, "siren": siren}
        )

        if details_response.status_code != 200:
            print(f"Erreur sur /entreprise pour SIREN {siren}")
            continue

        entreprise = details_response.json()

        dirigeants = entreprise.get("dirigeants", [])
        nom_dirigeant = "Inconnu"
        if dirigeants:
            d = dirigeants[0]
            nom_dirigeant = f"{d.get('prenom', '')} {d.get('nom', '')}".strip()

        resultats.append({
            "nom_entreprise": entreprise.get("nom_entreprise"),
            "siren": siren,
            "forme_juridique": entreprise.get("forme_juridique"),
            "siege": entreprise.get("siege", {}).get("adresse_ligne"),
            "code_naf": entreprise.get("activite", {}).get("code_naf"),
            "activite": entreprise.get("activite", {}).get("libelle"),
            "dirigeant": nom_dirigeant,
            "capital": entreprise.get("capital"),
            "date_creation": entreprise.get("date_creation")
        })

    return resultats
