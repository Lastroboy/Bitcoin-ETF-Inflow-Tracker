from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import tweepy
import time

# ========================
# Configurations
# ========================
URL = "https://farside.co.uk/btc/"
HTML_FILE = "farside_page.html"
CSV_FILE = "data_clean.csv"

# ========================
# Phase 1 : Scraping
# ========================
def save_html(url=URL, output_file=HTML_FILE):
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)
    driver.quit()
    print(f"[INFO] HTML sauvegardé dans {output_file}")

# ========================
# Phase 2 : Extraction & Nettoyage
# ========================
def load_html(file_path=HTML_FILE):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_table(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", class_="etf")
    if not tables:
        raise ValueError("[ERREUR] Aucune table trouvée.")
    return tables[0]  # On prend la première table

def clean_negative(value):
    if isinstance(value, str):
        if re.match(r'^\(.*\)$', value):
            value = "-" + value.strip("()")
        value = value.replace(",", "")
    return value

def parse_table(table):
    rows = []
    for tr in table.find_all("tr"):
        row = [th.get_text(strip=True) for th in tr.find_all(["th", "td"])]
        rows.append(row)

    # Suppression des lignes inutiles
    rows = rows[1:len(rows)-4]
    del rows[1:3]

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]

    # Renommer colonnes
    cols = list(df.columns)
    cols[0] = "Date"
    cols[-1] = "Total"
    df.columns = cols
    df = df.drop(columns="Total")

    # Conversion de la date
    df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")

    # Nettoyage des nombres
    for col in df.columns:
        if col != "Date":
            df[col] = df[col].apply(clean_negative)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Somme journalière
    df["Somme_ligne"] = df.sum(axis=1, numeric_only=True)

    return df

# ========================
# Phase 3 : Analyse & Message
# ========================
def generate_message(df):
    num_cols = df.select_dtypes(include="number").columns
    last_valid_index = df.dropna(subset=num_cols).index[-1]
    last_row = df.loc[last_valid_index]
    date_str = last_row["Date"].strftime("%d %b %Y")

    last_row_numeric = last_row[num_cols].apply(pd.to_numeric, errors='coerce')

    top_etf_name = last_row_numeric.drop('Somme_ligne').idxmax()
    top_etf_value = last_row_numeric.drop('Somme_ligne').max()
    worst_etf_name = last_row_numeric.drop('Somme_ligne').idxmin()
    worst_etf_value = last_row_numeric.drop('Somme_ligne').min()

    total_day = df.tail(1)["Somme_ligne"].iloc[0]  # scalar float
    total_7_days = df.tail(8)["Somme_ligne"].sum() # scalar float

    return (
        f"Inflow ETF BTC du {date_str} :\n"
        f"Top ETF : {top_etf_name} : {top_etf_value:.1f} M$\n"
        f"Pire ETF : {worst_etf_name} : {worst_etf_value:.1f} M$\n\n"
        f"Total du jour : {total_day:.1f} M$\n"
        f"Total sur 7 jours : {total_7_days:.1f} M$"
    )


# ========================
# Phase 4 : Post Twitter
# ========================
def post_to_twitter(message):
    # Récupération des clefs d'authentification
    with open("credentials.json", 'r') as f:
        creds = json.load(f)

    # Authentification
    consumer_key = creds["TWITTER_API_KEY"]
    consumer_secret = creds["TWITTER_API_SECRET"]
    access_token = creds["TWITTER_ACCESS_TOKEN"]
    access_token_secret = creds["TWITTER_ACCESS_SECRET"]

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(message)
        print("[INFO] Tweet publié avec succès.")
    except Exception as e:
        print(f"[ERREUR] Impossible de publier le tweet : {e}")

# ========================
# Point d’entrée
# ========================
def main():
    #for i in range(2):
        save_html() # scraper
        html = load_html()
        table = extract_table(html)
        df = parse_table(table)

        df.to_csv(CSV_FILE, index=False) # Facultatif 
        print(f"[INFO] Données nettoyées sauvegardées dans {CSV_FILE}")

        message = generate_message(df)

        print(message)
        #post_to_twitter(message)  # Publication sur Twitter

        #time.sleep(2*60)

if __name__ == "__main__":
    main()