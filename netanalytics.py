#!/usr/bin/env python
import argparse
import copy

from flask import Flask
from flask import redirect, render_template, request, session, url_for
import yaml

from db_connector import connector as conn
from schema_reader import schemareader

db_conn = None
app = Flask(__name__)
app.secret_key = (
    '\x16T@g\xcf\xdcGRzn\xf5\xc4\x068\xb9\xf7\xf7r]\xf6d\x96\x9a\xdd')


def configRead():
    config_dict = {}
    with open("config.yml", "r") as configread:
        try:
            config_dict = yaml.load(configread)
        except yaml.YAMLError as exc:
            print(exc)
    return config_dict


@app.route("/suggestions", methods=["POST", "GET"])
def suggestion_page():
    return render_template("suggestions.html")


@app.route("/", methods=["POST", "GET"])
def connection_info():
    error = None
    global db_conn
    if request.method == "POST":
        config_dict = {}
        config_dict['db.type'] = request.form['connector-type']
        config_dict['db.hostname'] = request.form['hostname']
        # connect to DB
        db_conn = conn.DBConnector(config_dict)
        db_conn.connect()
        print "Connection established."
        schema_reader = schema_read(db_conn)
        print "Schema Read"
        return redirect(url_for(".suggestion_page"))
    return render_template("conn-info.html", error=error)


def schema_read(db_conn):
    # Read schema
    schema_reader = schemareader.SchemaReader(db_conn)
    schema_reader.read()
    return schema_reader

if __name__ == "__main__":
    app.run()
