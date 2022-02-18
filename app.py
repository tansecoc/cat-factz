from flask import Flask, render_template, request, jsonify
import requests
import random
import itertools

app = Flask(__name__)

# https://catfact.ninja/
cat_facts = [
    "A female cat is called a queen or a molly.",
    "Cats have 30 teeth (12 incisors, 10 premolars, 4 canines, and 4 molars), while dogs have 42. Kittens have baby teeth, which are replaced by permanent teeth around the age of 7 months.",
    "A cat's normal pulse is 140-240 beats per minute, with an average of 195.",
    "Jaguars are the only big cats that don't roar.",
    "There are approximately 100 breeds of cat.",
    "Cats dislike citrus scent.",
    "Sir Isaac Newton is credited with creating the concept for the pet door that many cats use today to travel outdoors.",
    "Most cats adore sardines.",
    "The cat's footpads absorb the shocks of the landing when the cat jumps.",
    "All cats need taurine in their diet to avoid blindness. Cats must also have fat in their diet as they are unable to produce it on their own.",
    "In relation to their body size, cats have the largest eyes of any mammal.",
    "British cat owners spend roughly 550 million pounds yearly on cat food.",
    "Cats are extremely sensitive to vibrations. Cats are said to detect earthquake tremors 10 or 15 minutes before humans can.",
    "The cat who holds the record for the longest non-fatal fall is Andy. He fell from the 16th floor of an apartment building (about 200 ft/.06 km) and survived.",
    "Purring does not always indicate that a cat is happy and healthy - some cats will purr loudly when they are terrified or in pain.",
    ]

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
    return jsonify(cat_fact=random.choices(cat_facts))

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

if __name__ == "__main__":
    app.run("localhost", port=8000)
