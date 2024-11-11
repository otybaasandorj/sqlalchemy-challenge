# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from sqlalchemy import desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes"""

    return (
        f"Welcome to the Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).all()

    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)
    session.close()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()

    stations_list = [station[0] for station in results]
    return jsonify(stations_list)
    session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()[0]

    most_recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station).\
        filter(measurement.date >= one_year_ago).all()

    temps_list = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(temps_list)

    session.close()


@app.route('/api/v1.0/<start>')
def specified_start(start):
    session = Session(engine)
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")

        recent_date_row = session.query(measurement.date).order_by(desc(measurement.date)).first()
        recent_date = dt.datetime.strptime(recent_date_row[0], '%Y-%m-%d')

        tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).scalar()
        tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).scalar()
        tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).scalar()

        stats = {
            "Start Date": start,
            "End Date": recent_date_row[0],
            "Min Temp": tmin,
            "Max Temp": tmax,
            "Avg Temp": tavg
        }
        return jsonify(stats)

    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD format."}), 400

    except Exception as e:
         return jsonify({"error": str(e)}), 500
    
    session.close()


@app.route("/api/v1.0/<start>/<end>")
def specified_dates(start, end):
    session = Session(engine)
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")

        tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).scalar()
        tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).scalar()
        tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).scalar()

        stats = {
            "Start Date": start,
            "End Date": end,
            "Min Temp": tmin,
            "Max Temp": tmax,
            "Avg Temp": tavg
        }
        return jsonify(stats)

    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD format for both start and end dates."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    session.close()



if __name__ == "__main__":
   app.run(debug=True)
