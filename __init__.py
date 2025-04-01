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
 
 @app.route('/rapport/')
 def mongraphique():
     return render_template("graphique.html")
 
 @app.route('/histogramme/')
 def histogramme():
     return render_template("histogramme.html")
 
 @app.route('/contact/')
 def contact():
     return render_template("contact.html")

# Route pour afficher la page HTML de contact (Exercice 5)
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    confirmation = False
    if request.method == "POST":
        # Récupérer les données du formulaire (non enregistrées)
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        message = request.form.get("message")
        
        # Afficher un message de confirmation
        confirmation = True

    return render_template("contact.html", confirmation=confirmation)

# Route API pour extraire les commits (Exercice 6)
@app.route('/commits/')
def commits():
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
                continue
        
        return render_template("commits.html", commits=commit_minutes)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Impossible de récupérer les données depuis l'API GitHub.", "details": str(e)})

 
 if __name__ == "__main__":
   app.run(debug=True)
