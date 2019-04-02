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
engine = create_engine("sqlite:///static/db/summaryTables.sqlite")
# rds_connection_string = "root:qo#hwNXC)4u3@127.0.0.1/world"
# engine = create_engine(f'mysql://{rds_connection_string}')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Samples_Metadata = Base.classes.sample_metadata
test = Base.classes.stateGender

# print(Base.classes.keys(), file=sys.stderr)
# stBirthrate = Base.classes.statelevel
# ctBirthrate = Base.classes.countylevel

# Create our session (link) from Python to the DB
session = Session(engine) 
#print (Base.classes.keys())
# print(Base.classes.keys(), file=sys.stderr)


@app.route("/")
def index():
    """Return the homepage."""
    # return (f"This is a test")
    stmt = session.query(test).statement
    df = pd.read_sql_query(stmt, session.bind)

    # # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])



# @app.route("/data")
# def data():
#     """Return the data"""
#     return render_template("data.html")


# @app.route("/choropleth")
# def choropleth():
#     """Return the choropleth for US"""
#     return render_template("choropleth.html")


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
