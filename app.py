from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def pokemon_world():
    return "<p>Pokemon World</p>"

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return f'{email} {password}'
    else:
        return render_template('login.html')
    
def get_pokemon_data(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "hp": data["stats"][0]["base_stat"],
            "defense": data["stats"][3]["base_stat"],
            "attack": data["stats"][1]["base_stat"],
            "sprite": data["sprites"]["front_shiny"],
            "ability": data["abilities"][0]["ability"]["name"]
        }
    else:
        return {"error": "Pokemon not found or API error"}

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name_or_id')
        pokemon_data = get_pokemon_data(name)
        return render_template('pokemon.html', pokemon=pokemon_data)
    else:
       return render_template('pokemon.html')

if __name__ == '__main__':
    app.run(debug=True)