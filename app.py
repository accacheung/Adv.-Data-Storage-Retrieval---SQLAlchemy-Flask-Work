# Import Flask, sqlalchemy
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)


# Flask Routes
# Adding "home" to avoid landing on 404 Error page, also to show available api routes.
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return dates and temperature observations from last year."""
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").order_by(Measurement.date)
    
     # Create a dictionary from the row data and append to a list of all observations.
    all_precipitations = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of Temperature Observations (tobs) for the previous year."""
    # Query all tobs values
    results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    all_observations = list(np.ravel(results))

    return jsonify(all_observations)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. 
@app.route("/api/v1.0/<start>")
def start(start):
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    # Set datetime format as '%Y-%m-%d'
    start= dt.datetime.strptime(start, '%Y-%m-%d')
   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    all_temp_start = list(np.ravel(results))

    return jsonify(all_temp_start)


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    # Set datetime format as '%Y-%m-%d'
    start= dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    all_temp = list(np.ravel(results))

    return jsonify(all_temp)


if __name__ == '__main__':
    app.run(debug=True)
    
 