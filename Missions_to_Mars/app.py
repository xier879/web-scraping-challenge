from flask import Flask, render_template
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
#classwork 12-3-08
app = Flask(__name__)
# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.MarsMission_db
collection=db.mars_data

@app.route("/scrape")
def scrape():
    mars_scrape = scrape_mars.scrape()
    collection.insert_one(mars_scrape)
@app.route("/")
def index():
    mars = list(db.collection.find())
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
    app.run(debug=True)




