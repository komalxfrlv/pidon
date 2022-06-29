from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tubeoverdriver:dWSrGA@localhost/GPS'

db = SQLAlchemy(app)


@app.route('/')
@cross_origin()
def last_location():
    track = Tracks.query.order_by(Tracks.id.desc()).first()
    return jsonify(
        {
            "lat": track.latitude,
            "lng": track.longitude,
            "datetime": track.datetime,
         }
    )


@app.route('/sendLocation', methods=['POST'])
def send_location():
    lat = request.form['lat']
    lng = request.form['lng']
    location = Tracks(latitude=lat, longitude=lng)
    db.session.add(location)
    db.session.commit()
    return jsonify('send..')


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(80), unique=False, nullable=False)
    longitude = db.Column(db.String(120), unique=False, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
