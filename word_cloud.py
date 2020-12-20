import google
import requests
from googlesearch import search
import pandas as pd
from bs4 import BeautifulSoup
import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from custom_stopwords import custom_stopwords
import os.path

drama_db = pd.read_csv("drama_db.csv")


def extract_content(url_list):
    web_content_cleaned_all = []
    for url in url_list:
        try:
            web_content = BeautifulSoup(requests.get(url, stream=True).content, "lxml").text
        except (requests.exceptions.MissingSchema, requests.exceptions.ContentDecodingError):
            continue
        web_content_cleaned = [val.lower() for val in web_content.split(' ') if val.isalpha() or val.isnumeric()]
        web_content_cleaned_all.extend(web_content_cleaned)

    # with open("content.txt", "wb") as fp:
    #     pickle.dump(web_content_cleaned_all, fp)
    
    return web_content_cleaned_all

def process_data(content):
    lemmatizer = WordNetLemmatizer()
    qry_words = list(set(title.lower().split(' ') + [lemmatizer.lemmatize(w) for w in title.lower().split(' ')]))
    stop_words = set(list(set(stopwords.words('english'))) + qry_words + custom_stopwords)
    clean_content = [lemmatizer.lemmatize(word) for word in content if word not in stop_words]
    return clean_content

if __name__ == "__main__":
    for i in range(10):
        title = drama_db.iloc[i, 1]
        if not os.path.exists(f'./wordclouds/{title}.png'):
            res = search(title + ' kdrama', num_results=30)
            print(f"Extracting the contents of {title}")
            content = extract_content(res)
            # with open("content.txt", "rb") as fp:
            #     content = pickle.load(fp)
            print(f"Processing the contents of {title}")
            clean_content = process_data(content)
            print(f"Generating Word Cloud for {title}")
            clean_content = ' '.join(clean_content)
            wordcloud = WordCloud(max_font_size=100, max_words=100, background_color='white', random_state=0).generate(clean_content)
            wordcloud.to_file(f'./wordclouds/{title}.png')
