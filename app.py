from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('movies_schedule.json', 'r') as json_file:
        movies_data = json.load(json_file)
    return render_template('index.html', movies=movies_data)

@app.route('/movies')
def movies():
    with open('movies_schedule.json', 'r') as json_file:
        data = json.load(json_file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
