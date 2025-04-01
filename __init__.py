@app.route('/api/commits/')
def api_commits():
    # URL de l'API GitHub pour récupérer les commits
    url = "https://api.github.com/repos/projetuser/5MCSI_Metriques/commits"
    
    try:
        # Récupération des données depuis l'API GitHub
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        
        # Extraire les minutes des dates des commits
        commit_minutes = []
        for commit in data:
            commit_date = commit['commit']['author']['date']
            # Convertir la date et extraire la minute
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            commit_minutes.append(date_object.minute)

        # Comptabiliser le nombre de commits par minute
        minute_count = {minute: commit_minutes.count(minute) for minute in set(commit_minutes)}

        return jsonify(minute_count)
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Route HTML pour afficher la page des commits (Exercice 6)
@app.route('/commits/')
def commits():
    return render_template("commits.html")
