import os
from flask import Flask, flash, request, render_template, jsonify
import random

RESULTS_FILE = "gpt2_results.txt"

titles = []
file_dir = os.path.dirname(os.path.abspath(__file__))
with open(file_dir + "/data/" + RESULTS_FILE, encoding = 'utf-8') as fle:
    for line in fle:
        titles.append(line)
total_items = len(titles)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template('index.html')

@app.route("/title", methods = ['GET'])
def title():
    index = random.randint(0, total_items - 1)
    title = titles[index]
    return jsonify(
        title = title
    )

if __name__ == "__main__":
    app.run(port = 9002)