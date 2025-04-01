from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
from urllib.request import urlopen

app = Flask(__name__)

# Route principale pour la page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Exercice 2 : Création d'une nouvelle route pour la page de contact
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

# Exercice 3 : Les données d'une API (OpenWeatherMap)
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# Exercice 3 Bis : Affichage du fichier graphique.html
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Exercice 3 Ter : Transfert de données pour le graphique Google Charts
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# Exercice 6 : Combien de commits pour ce projet ?
@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    # Extraire les minutes des commits
    commit_minutes = []
    for commit in data:
        commit_date = commit['commit']['author']['date']
        # Convertir la date et extraire la minute
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_object.minute)

    # Comptabiliser le nombre de commits par minute
    minute_count = {minute: commit_minutes.count(minute) for minute in set(commit_minutes)}

    return render_template('commits.html', minute_count=minute_count)

if __name__ == "__main__":
    app.run(debug=True)
