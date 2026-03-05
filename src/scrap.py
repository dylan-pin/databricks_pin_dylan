import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import time
import os
from pathlib import Path
from datetime import datetime
from src.config import *
from datetime import date

# dossier où sont tes fichiers CSV
dossier = Path("..") / Path(URL_FOLDER)
# date du jour sans l'heure
today_str = date.today().isoformat()  # e.g. "2026-03-05"
# lister tous les fichiers .csv du dossier
all_files = list(dossier.glob("*.csv"))
# filtrer ceux qui contiennent la date du jour dans le nom
date_files = [f for f in all_files if today_str in f.name]
print("Fichiers du jour :", date_files)
# liste pour accumuler tous les URLs
all_urls = []
# parcourir chaque fichier trouvé
for f in date_files:
    # lire le CSV
    df_temp = pd.read_csv(f, sep=",")
    # ajouter les URLs à la liste
    if "url" in df_temp.columns:
        all_urls.extend(df_temp["url"].tolist())
# dédupliquer
urls = list(set(all_urls))
print(urls)

output_file = ".." / Path(URL_FOLDER) / f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} resultats_meamedica.csv"
# print(output_file)

# Selectionner les métadonnées à extraire
data = {
    "date": [],
    "sexe": [],
    "age": [],
    "medicament": [],
    "indications": [],
    "efficacite": [],
    "effets_secondaires": [],
    "avis": [],
    "url": []
}

with tqdm(total=len(urls), desc="Scraping meamedica.fr") as pbar:
    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                pbar.update(1)
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # trouver les avis
            avis_blocks = soup.find_all("div", class_="vote rounded btn-left")
            if not avis_blocks:
                pbar.update(1)
                continue

            for block in avis_blocks:
                # extraire les champs
                date = ""
                sexe = ""
                age = ""
                medicament = ""
                indications = ""
                efficacite = ""
                effets_secondaires = ""
                avis_text = ""

                text_section = block.find_all("div", class_="subText")
                review_section = block.find_all("div", class_="review")
                rating_section = block.find_all("div", class_="ratings")

                # date | sexe | age + medicament | indications
                for t in text_section:
                    ecrit = t.get_text(separator="\n").strip()
                    match = re.search(r"(\d{2}/\d{2}/\d{4}) \| ([^|]+) \| (\d+)", ecrit)
                    if match:
                        date = match.group(1)
                        sexe = match.group(2).strip()
                        age = match.group(3)

                    lignes = ecrit.split("\n")
                    if len(lignes) >= 4:
                        medicament = lignes[2].strip()
                        indications = lignes[3].strip()

                for r in review_section:
                    avis_text = r.get_text().strip()

                for rate in rating_section:
                    for label in rate.find_all("span"):
                        if label.has_attr("title"):
                            if "efficace" in label["title"]:
                                efficacite = label["title"]
                            else:
                                effets_secondaires = label["title"]

                # ne conserver que si on a une vraie info
                if date or avis_text:
                    data["date"].append(date)
                    data["sexe"].append(sexe)
                    data["age"].append(age)
                    data["medicament"].append(medicament)
                    data["indications"].append(indications)
                    data["efficacite"].append(efficacite)
                    data["effets_secondaires"].append(effets_secondaires)
                    data["avis"].append(avis_text)
                    data["url"].append(url)

            time.sleep(1)

        except Exception as e:
            print(f"Erreur sur {url}: {e}")

        pbar.update(1)

# Enregistrer les résultats dans un fichier CSV
df = pd.DataFrame(data)
df.to_csv(output_file, index=False, encoding="utf-8")