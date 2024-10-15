
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
def fetch_and_store_data():
    print("Fetching data...")
    # Define the CoinGecko API URL
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd'

    # Make a GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract prices
        bitcoin_price = data['bitcoin']['usd']
        ethereum_price = data['ethereum']['usd']

        # Get the current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a DataFrame
        crypto_data = {
            'cryptocurrency': ['Bitcoin'],
            'price_usd': [bitcoin_price],
            'timestamp': [current_time]
        }

        df = pd.DataFrame(crypto_data)
        st.subheader("Real-Time Bitcoin Prices")
        st.write(df)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
def scrape_news():
    url = 'https://www.coindesk.com/livewire/'  # URL du site
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h4_tags = soup.find_all('h4', class_='typography__StyledTypography-sc-owin6q-0 dtjHgI')
        return [tag.text for tag in h4_tags]  # Retourne la liste des titres extraits
    return []


def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Renvoie un score de sentiment (-1 = négatif, 1 = positif)


news_data = scrape_news()
sentiment_data = [(news, analyze_sentiment(news)) for news in news_data]

# Créer un DataFrame pour visualiser les résultats
df = pd.DataFrame(sentiment_data, columns=['News', 'Sentiment'])
average_sentiment = df['Sentiment'].mean()
fetch_and_store_data()
# Affichage du tableau de bord Streamlit
st.title("Tableau de bord sur les sentiments des news de Bitcoin")
st.write("Ce tableau de bord affiche les bonnes et mauvaises nouvelles en temps réel pour Bitcoin.")

# Créer des graphiques interactifs avec Plotly
fig = px.bar(df, x='News', y='Sentiment', color='Sentiment',
             title='Sentiment des news sur Bitcoin',
             labels={'News': 'Nouvelles', 'Sentiment': 'Score de Sentiment'})

st.plotly_chart(fig)

# Ajouter un tableau de visualisation des news
st.write("Détails des nouvelles et leurs sentiments :")
st.dataframe(df)

# Filtrer et afficher les bonnes et mauvaises nouvelles
good_news = df[df['Sentiment'] > 0.1]
bad_news = df[df['Sentiment'] < -0.1]

st.subheader("Bonne nouvelle sur Bitcoin")
st.write(good_news[['News', 'Sentiment']])

st.subheader("Mauvaise nouvelle sur Bitcoin")
st.write(bad_news[['News', 'Sentiment']])
st.subheader("Overall Sentiment Analysis")

if average_sentiment > 0.1:
    st.success("Most news about Bitcoin is positive! The coin's value may increase.")
elif average_sentiment < -0.1:
    st.warning("Most news about Bitcoin is negative! The coin's value may decrease.")
else:
    st.info("No significant sentiment from the news. Bitcoin's value may remain stable.")