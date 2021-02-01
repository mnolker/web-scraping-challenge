# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template('index.html', marsdata=mars_data)


@app.route('/scrape')
def scrape():
    mars_data = mongo.db.marsdata
    data = scrape_mars.scrape()
    marsdata.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)