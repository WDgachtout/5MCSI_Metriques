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

@app.route("/contact/", methods=["GET", "POST"])
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
         
if __name__ == "__main__":
  app.run(debug=True)
