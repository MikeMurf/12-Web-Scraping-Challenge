### Step 2.2 - MongDB and Flask Application
#### Requirement is to "create a route called '/scrape' that will import your 'scrape_mars.py' script and call your 'scrape' function".

#   Load dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

#   Import the Function Defined in 'scrape_mars.py'
import scrape_mars

#   Create an instance of flask
app = Flask(__name__)

#   Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#   Route to render index.html template using data from the Mongo database
@app.route("/")
def home():
    #   Find one record of data from the mongo database
    mars_data_1 = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars_data_1)

#   Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    #   Run the scrape function
    mars_data_2 = scrape_mars.scrape()
    #   Insert the record
    mongo.db.collection.update_one({}, {"$set": mars_data_2}, upsert=True)
    #   Redirect back to home page
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()


