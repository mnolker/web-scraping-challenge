# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    marsdata = mongo.db.marsdata.find_one()
    return render_template('index.html', marsdata=marsdata)


@app.route("/scrape")
def scrape():
    
    # Run the scrape function
    marsdata = mongo.db.marsdata
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    marsdata.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

# alternative scrape
    # marsdata = mongo.db.marsdata
    # mars_data = scrape_mars.scrape()
    # marsdata.update(
    #     {},
    #     mars_data,
    #     upsert=True
    # )
    # return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)