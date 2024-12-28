from flask import Flask, jsonify, render_template
from selenium_scraper import scrape_trending_topics  # Your scraper logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # HTML file to run the script

@app.route('/run-selenium', methods=['GET'])
def run_selenium():
    data = scrape_trending_topics()  # Function to fetch data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
