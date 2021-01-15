import json
from flask import Flask, render_template, redirect, request


app = Flask(__name__)


FILENAME = "request_counts.txt"


def write_requests_into_file(method):
    requests = get_requests_from_file()
    requests[method] = requests.get(method, 0) + 1
    with open(FILENAME, 'w') as file:
        file.write(json.dumps(requests))


def get_requests_from_file():
    requests = {}
    with open(FILENAME, 'r') as file:
        requests_json = file.read()
        requests = json.loads(requests_json)
    return requests


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/request-counter', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_counter_form():
    if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
        write_requests_into_file(request.method)
    return redirect('/')


@app.route('/statistics')
def display_statistics():
    requests = get_requests_from_file()
    return render_template('statistics.html', get=requests.get('GET', 0), post=requests.get('POST', 0), put=requests.get('PUT', 0), delete=requests.get('DELETE', 0))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
    
