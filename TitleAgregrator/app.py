from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def scrape_titles(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get page with status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', id='content') 

    titles = []
    for article in articles:
        title_tag = article.find('h2', class_='c-entry-box--compact__title')  #Based on the actual HTML structure of the website
        date_tag = article.find('time', class_='c-byline__item')  #Based on the actual HTML structure of the website
        if title_tag and date_tag:
            title = title_tag.text.strip()
            link = title_tag.find('a')['href'] if title_tag.find('a') else '#'  #Based on the actual HTML structure of the website
            date = datetime.strptime(date_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')  #Based on the actual HTML structure of the website
            if date >= datetime(2022, 1, 1):
                titles.append({'title': title, 'link': link, 'date': date})

    return titles

@app.route('/')
def index():
    titles = scrape_titles('https://www.theverge.com')
    titles = sorted(titles, key=lambda x: x['date'], reverse=True)
    return render_template('index.html', titles=titles)

if __name__ == '__main__':
    app.run(debug=True)


