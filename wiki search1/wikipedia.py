from flask import Flask, request, render_template_string, session
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'una_chiave_segreta_molto_sicura'

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        if 'download' in request.form:
            term = request.form['term']
            try:
                # Cercare su Wikipedia
                search_url = f"https://it.wikipedia.org/wiki/{term}"
                response = requests.get(search_url)
                response.raise_for_status()
                
                # Analizzare il contenuto della pagina
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Raccogliere tutto il contenuto significativo
                content = ''
                for para in soup.find_all('p'):
                    if para.get_text(strip=True):
                        content += para.get_text() + '\n'
                
                # Salvare il contenuto in un file di testo
                with open(r'C:\Users\fabio\OneDrive\Desktop\wiki search1\info.txt', 'w', encoding='utf-8') as file:
                    file.write(content.strip())
                
                message = 'I dati della pagina Wikipedia sono stati scaricati con successo.'
                session['downloaded'] = True
            except requests.exceptions.RequestException as e:
                message = f"Un errore è occorso: {e}"

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web Scraper</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; }
            form { max-width: 300px; margin: 50px auto; }
            input[type="text"], input[type="submit"] { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
            input[type="submit"] { border: 1px solid #ddd; background-color: #5cb85c; color: white; }
        </style>
    </head>
    <body>
        <form method="POST">
            <input type="text" name="term" placeholder="Inserisci il termine di ricerca qui">
            <input type="submit" name="download" value="Scarica Dati">
        </form>
        {{ message }}
    </body>
    </html>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True)
