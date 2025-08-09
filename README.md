# Bitcoin ETF Inflow Tracker

Un outil de scraping et d'analyse automatisé pour suivre les flux d'investissement (inflows/outflows) des ETF Bitcoin et générer des synthèses quotidiennes.

## 🎯 Objectif

Ce projet automatise la collecte et l'analyse des données de flux financiers des ETF Bitcoin depuis le site Farside Investors, permettant de comprendre rapidement la conjoncture du marché des ETF BTC à travers un message de synthèse clair et concis.

## 📊 Fonctionnalités

- **Scraping automatisé** : Extraction des données depuis farside.co.uk
- **Nettoyage intelligent** : Traitement des valeurs négatives et formatage des données
- **Analyse comparative** : Identification du meilleur et du pire ETF du jour
- **Synthèse périodique** : Calcul des totaux quotidiens et hebdomadaires
- **Publication automatique** : Intégration Twitter pour partager les analyses
- **Export des données** : Sauvegarde en CSV pour analyses ultérieures

## 🛠️ Technologies utilisées

- **Python 3.x**
- **Selenium** : Scraping web dynamique
- **BeautifulSoup** : Parsing HTML
- **Pandas** : Manipulation et analyse des données
- **Tweepy** : Intégration API Twitter
- **Chrome WebDriver** : Automatisation du navigateur

## 🚀 Utilisation

```bash
python main.py
```

Le script effectue automatiquement :
1. Le scraping de la page Farside
2. L'extraction et le nettoyage des données
3. L'analyse et la génération du message de synthèse
4. L'affichage du résultat (et optionnellement la publication sur Twitter)

## 📈 Format de sortie

Le script génère un message de synthèse au format :

```
Inflow ETF BTC du 08 Aug 2025 :
Top ETF : IBIT : 360.0 M$
Pire ETF : ARKB : -0.4 M$

Total du jour : 403.9 M$
Total sur 7 jours : 279.5 M$
```

## 📁 Structure du projet

```
├── main.py              # Script principal
├── credentials.json     # Clés API Twitter (à créer)
├── data_clean.csv      # Données nettoyées exportées
├── farside_page.html   # Page HTML scrappée
└── README.md           # Documentation
```

## 🔄 Architecture du code

Le projet est organisé en 4 phases principales :

1. **Scraping** : Récupération de la page web avec Selenium
2. **Extraction & Nettoyage** : Parsing HTML et traitement des données
3. **Analyse** : Génération des métriques et du message de synthèse
4. **Publication** : Diffusion sur Twitter (optionnel

## ⚠️ Notes importantes

- Le script est configuré pour scraper `farside.co.uk/btc/`
- Les valeurs entre parenthèses sont automatiquement converties en valeurs négatives
- Le calcul des totaux sur 7 jours inclut les 8 derniers jours de données disponibles
- La publication Twitter est commentée par défaut dans le code

- Le script analyse les principaux ETF Bitcoin :
    • IBIT (BlackRock) 
    • FBTC (Fidelity) 
    • BITB (Bitwise) 
    • ARKB (ARK 21Shares) 
    • BTCO, EZBC, BRRR, HODL, BTCW 
    • GBTC (Grayscale) 
    • BTC (Autres) 

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

## ⚖️ Avertissement

Ce projet est à des fins éducatives et d'information. Les données financières doivent être vérifiées avant toute prise de décision d'investissement.
