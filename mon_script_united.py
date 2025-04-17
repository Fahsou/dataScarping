from bs4 import BeautifulSoup
from fpdf import FPDF
import os

#chemin de dossier
dossier_mhtml = "toScarpe"
#initialise le pdf
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Offres d'emploi Portal Job", ln=True, align="C")

#encode et decode du fpdf
def nettoie_text(txt):
    return txt.encode('latin-1', 'ignore').decode('latin-1')

#extraction du lien dans content-location
def extractLink(chemin_fichier):
    with open(chemin_fichier, "r", encoding="utf-8", errors='ignore') as f:
        for ligne in f:
            if ligne.lower().startswith("content-location:"):
                return ligne.split(":", 1)[1].strip()
            if "<!DOCTYPE html" in ligne:
                break
    return "lien non trouve"

compteur =1
#parcour de dossier
for nom_fichier in os.listdir(dossier_mhtml):
    if nom_fichier.endswith(".mhtml"):
        chemin = os.path.join(dossier_mhtml, nom_fichier)
        try:
            with open(chemin, "r", encoding="utf-8", errors="ignore") as fichier:
                soup = BeautifulSoup(fichier, "lxml") #initialisation BeautifulSoup

                # Titre
                titre_tag = soup.select_one("div.item_tab.active h2")
                titre = titre_tag.get_text(strip=True) if titre_tag else "Titre non trouvé"

                # Date
                date_tag = soup.select_one("span.offers-date")
                date = date_tag.get_text(strip=True) if date_tag else "Date non trouvée"

                #lien
                lien = extractLink(chemin)

                # Détails
                detail_blocks = soup.select("div.item_detail, section.item_detail")[1:]
                textes = [block.get_text(strip=True, separator="\n") for block in detail_blocks]
                 
                # activité, mission, profil sous-titres a inserer dans le pdf
                sous_titres = ["À propos de l'entreprise", 
                    "Missions", 
                    "Profil"]

                # Écriture dans le PDF
                pdf.set_font("Arial", "B", 14)
                pdf.multi_cell(0, 10, f" {compteur}. {nettoie_text(titre)}")

                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Date de publication : {date}", ln=True)

                
                if "http" in lien:
                    pdf.set_text_color(0,0,0)
                    pdf.set_font("Arial", "", 12)
                    pdf.cell(0, 10, "Lien de l'offre:", ln = True)

                    pdf.set_font("Arial", "U", 12)
                    pdf.set_text_color(0, 0, 255)
                    pdf.multi_cell(0, 10, f"{lien}")
                    pdf.set_text_color(0,0,0)
                else:
                    pdf.multi_cell(0, 10, f"{lien}")

                for i, texte in enumerate(textes):
                    pdf.set_font("Arial", "B", 12)
                    titre = sous_titres[i] if i < len(sous_titres) else f"Section {i+1}"
                    pdf.multi_cell(0, 10, titre)

                    pdf.set_font("Arial", "", 12)
                    def nettoie_text(txt):
                        return txt.encode('latin-1', 'ignore').decode('latin-1')
                    pdf.multi_cell(0, 7, nettoie_text(texte))
                
                pdf.ln(10)
                compteur+=1

        except Exception as e:
            print(f"Erreur avec le fichier {nom_fichier} : {e}")

pdf.output("offres_portaljob_uni.pdf")
print("PDF generated.")

