import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# creating an instance of Flask

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/missionToMars')


@app.route("/")
def init():

    results = mongo.db.collection.find_one()
    return render_template("index.html", result=results)


@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()
    mongo.db.collection.update({}, data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
