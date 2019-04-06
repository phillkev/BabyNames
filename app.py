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

engine = create_engine("sqlite:///db/summaryTables.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Samples_Metadata = Base.classes.sample_metadata
print(Base.classes.keys(), file=sys.stderr)
statecount = Base.classes.statecount
wordcloud = Base.classes.wordcloud
yearName = Base.classes.yearName


# Create our session (link) from Python to the DB
session = Session(engine) 

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html", statecount=statecount, wordcloud=wordcloud)


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
    return jsonify(results)


@app.route("/cloudchartdata2")
def cloudchartdata2():

    stmt = session.query(wordcloud).statement
    df = pd.read_sql_query(stmt, session.bind)

    data = df.to_json(orient='records')
    return jsonify(data)


@app.route("/linechart/<userSelection>")
def linechart(userSelection):

    stmt = session.query(yearName).statement
    df = pd.read_sql_query(stmt, session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    print(df)
    sample_data = df[df.Name.str.lower() == userSelection]
    print(sample_data)
    print(userSelection)
    data = sample_data.to_json(orient='records')
    return data

@app.route("/chlorodata")
def chlorodata():

    stmt = session.query(statecount).statement
    df = pd.read_sql_query(stmt, session.bind)

    data = df.to_json(orient='records')
    return jsonify(data)


if __name__ == "__main__":
    app.run()
