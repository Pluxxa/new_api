from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    quote = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        news = get_news()
        quote = get_random_quote()
        quote['content'] = translate_text(quote['content'])
        quote['author'] = translate_text(quote['author'])
    return render_template("index.html", weather=weather, news=news, quote=quote)

def get_weather(city):
    api_key = "fedff6ea86d8d0f6531ed2c81b1efcac"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    return response.json()

def get_news():
    api_key = '3194db55657d42f89143f20e60513832'
    url = f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={api_key}'
    response = requests.get(url)
    return response.json().get('articles', [])

def get_random_quote():
    url = 'https://api.quotable.io/random'
    response = requests.get(url)
    return response.json()

def translate_text(text):
    translated = translator.translate(text, dest='ru')
    return translated.text

if __name__ == '__main__':
    app.run(debug=True)
