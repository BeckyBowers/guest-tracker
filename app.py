#!/usr/bin/env python

import argparse
import csv
from flask import Flask, render_template

import app_config
from render_utils import make_context, urlencode_filter
import static

app = Flask(app_config.PROJECT_NAME)

app.jinja_env.filters['urlencode'] = urlencode_filter

@app.route('/')
def tracker():
    """
    {
        "John Boehner": [
            {
                "Date": "1/9/2014",
                "Show": "Meet the Press
            },
            {
                "Date": "1/20/2014",
                "Show": "Fox and Friends"
            }
        ],
        "Nancy Pelosi": [
            {
                "Date": "1/9/2014",
                "Show": "Meet the Press
            },
            {
                "Date": "1/20/2014",
                "Show": "Fox and Friends"
            }
        ]
    }
    """
    context = make_context()
    context['guests'] = {}

    with open('data/guest-tracker.csv', 'rb') as readfile:
        csvreader = csv.DictReader(readfile)

        for row in csvreader:
            if row['Person'] != '':

                if not context['guests'].get(row['Person'], None):
                    context['guests'][row['Person']] = []

                context['guests'][row['Person']].append(row)


    return render_template('index.html', **context)

@app.route('/widget.html')
def widget():
    """
    Embeddable widget example page.
    """
    return render_template('widget.html', **make_context())

@app.route('/test_widget.html')
def test_widget():
    """
    Example page displaying widget at different embed sizes.
    """
    return render_template('test_widget.html', **make_context())

@app.route('/test/test.html')
def test_dir():
    return render_template('index.html', **make_context())

app.register_blueprint(static.static)

# Boilerplate
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    server_port = 8000

    if args.port:
        server_port = int(args.port)

    app.run(host='0.0.0.0', port=server_port, debug=app_config.DEBUG)
