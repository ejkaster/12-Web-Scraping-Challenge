from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Use flask_pymongo to set up mongo connection
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# route
@app.route("/")
def home(): 

    # Find data
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    mars = scrape_mars.scrape_mars_data()
    mongo.db.collection.update({}, mars, upsert=True)

    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)