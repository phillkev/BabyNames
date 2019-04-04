import os
import sys

import pandas as pd
import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# rds_connection_string = "root:qo#hwNXC)4u3@127.0.0.1/usnatality"
# app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{rds_connection_string}'
# db = SQLAlchemy(app)
engine = create_engine("sqlite:///db/summaryTables.sqlite")
# rds_connection_string = "root:qo#hwNXC)4u3@127.0.0.1/world"
# engine = create_engine(f'mysql://{rds_connection_string}')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Samples_Metadata = Base.classes.sample_metadata
print(Base.classes.keys(), file=sys.stderr)
stateGender = Base.classes.stateGender
wordcloud = Base.classes.wordcloud
yearName = Base.classes.yearName


# Create our session (link) from Python to the DB
session = Session(engine) 


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html", stateGender=stateGender, wordcloud=wordcloud)


@app.route("/data")
def data():
    """Return the homepage."""
    # return (f"This is a test")
    stmt = session.query(wordcloud).statement
    df = pd.read_sql_query(stmt, session.bind)

    # # Return a list of the column names (sample names)
    return jsonify(list(df.columns))


@app.route("/name")
def name():
    """Return the choropleth for US"""
    return render_template("name.html", yearName=yearName)

@app.route("/cloudchartdata")
def cloudchartdata():
    """Return the MetaData for a given sample."""
    sel = [
        wordcloud.Name,
        wordcloud.total_count,
    ]

    results = session.query(*sel).all()
    print(results)
    # Create a dictionary entry for each row of metadata information
    top50 = {}
    for result in results:
        top50["Name"] = result[0]
        top50["total_count"] = result[1]

    print(top50)
    return jsonify(top50)


@app.route("/cloudchartdata2")
def cloudchartdata2():

    stmt = session.query(wordcloud).statement
    df = pd.read_sql_query(stmt, session.bind)

    data = df.to_json(orient='records')
    return jsonify(data)

# @app.route("/chloropleth")
# def chloropleth():
#     """Return the choropleth for US"""
#     return render_template("chloropleth.html")


# @app.route("/bubblechart")
# def bubble():
#     """Return the bubble chart"""
#     return render_template("bubblechart.html")

# @app.route("/linechart")
# def line():
#     """Return the line chart"""
#     return render_template("linechart.html")

if __name__ == "__main__":
    app.run()
