from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()
    
    # Return template and data
    return render_template("index.html", mars_info=mars_data)


@app.route("/scrape")
def scrape():
    print("Please wait while we scrape...")

    # time.sleep(10)
    # Run the scrape function and save the results to a variable
    # @TODO: YOUR CODE HERE!
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    # @TODO: YOUR CODE HERE!
    mongo.db.collection.update({},mars_data,upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
