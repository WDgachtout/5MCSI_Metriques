from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

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

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

from flask import Flask, jsonify, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/commits/')
def commits_graph():
    # URL de l'API GitHub pour récupérer les commits
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Récupération des données depuis l'API GitHub
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        commits_data = response.json()
        
        # Extraire les minutes des dates des commits
        commit_minutes = []
        for commit in commits_data:
            try:
                date_string = commit['commit']['author']['date']
                date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
                commit_minutes.append(date_object.minute)
            except KeyError:
                # Ignorer les commits sans clé 'date'
                continue
        
        # Compter les occurrences des minutes
        minute_counts = {}
        for minute in commit_minutes:
            if minute not in minute_counts:
                minute_counts[minute] = 0
            minute_counts[minute] += 1
        
        # Préparer les données pour le graphique
        graph_data = [{"minute": minute, "count": count} for minute, count in sorted(minute_counts.items())]
        
        return render_template("commits.html", graph_data=graph_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Impossible de récupérer les données depuis l'API GitHub.", "details": str(e)})

      
if __name__ == "__main__":
  app.run(debug=True)
