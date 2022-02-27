from flask import Flask, render_template, request, jsonify
import requests
import random
import itertools

app = Flask(__name__)

# breed, image, low_weight, high_weight
cat_breed_dict = { 
    1: ("British Shorthair", "british_shorthair_1.jpeg", 7, 17),
    2: ("Maine Coon", "maine_coon_1.jpeg", 8, 18),
    3: ("Persian", "persian_1.jpeg", 7, 12),
    4: ("Siamese", "siamese_1.jpeg", 8, 15)
    }

cat_breed_dict_cycle = itertools.cycle(cat_breed_dict)

@app.route("/", methods=['GET'])
def home():
    """Home Page"""
    return render_template("home.html")

@app.route('/background_process')
def background_process():
    response = requests.get("https://catfact.ninja/fact")
    json = response.json()
    fact = json['fact']
    return jsonify(cat_fact=fact)

# https://stackoverflow.com/questions/58924015/how-to-display-image-in-flask-after-a-button-is-pressed
@app.route("/getimage")
def get_img():
    breed, image, low_weight, high_weight = cat_breed_dict[next(cat_breed_dict_cycle)]
    return '{}|{}|{}|{}'.format(image, breed, low_weight, high_weight)

@app.route("/catfactsapi")
def cat_fact_api():
    response = requests.get("https://catfact.ninja/fact")
    json = response.json()
    fact = json['fact']
    return fact

@app.route("/toggleWeight", methods=['GET','POST'])
def convert_weight():
    response_payload = {}
    
    if request.method == "POST":
        low_weight = request.form['low_weight']
        high_weight = request.form['high_weight']
        low_unit = request.form['low_unit']
        high_unit = request.form['high_unit']

        if low_unit == 'lb':
            current_unit = 'lb'
            convert_unit = 'kg'
        else:
            current_unit = 'kg'
            convert_unit = 'lb'

        endpoint = "https://cs361-mass-unit-converter.herokuapp.com/"

        low_weight_query = endpoint + low_weight + "/" + current_unit + "/" + convert_unit
        low_weight_response = requests.get(low_weight_query)
        low_weight_json = low_weight_response.json()

        high_weight_query = endpoint + high_weight + "/" + current_unit + "/" + convert_unit
        high_weight_response = requests.get(high_weight_query)
        high_weight_json = high_weight_response.json()

        response_payload['low_weight'] = str(round(float(low_weight_json['result_mass']), 1))
        response_payload['high_weight'] = str(round(float(high_weight_json['result_mass']), 1))
        response_payload['unit'] = low_weight_json['result_units']

    return response_payload

if __name__ == "__main__":
    app.run("localhost", port=8000)

