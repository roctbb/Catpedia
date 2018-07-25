from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://user:As1234@ds245971.mlab.com:45971/catpedia')
db = client['catpedia']
cat_collection = db['cats']

app = Flask(__name__)


@app.route('/')
def index():
    cats = list(cat_collection.find())
    return render_template('index.html', cats=cats)

@app.route('/cat')
def details():
    id = request.args.get('id', '')
    if not id:
        return "404"
    cat = cat_collection.find_one({"_id": ObjectId(id)})
    return render_template('details.html', cat=cat)

@app.route('/add')
def add():
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    image = request.args.get('image', '')

    if name and description and image:
        cat = {
            "name": name,
            "description": description,
            "image": image
        }
        cat_collection.insert_one(cat)
        return redirect('/cat?id='+str(cat['_id']))
    return render_template('add.html')


app.run(debug=True, port=8082, host='0.0.0.0')