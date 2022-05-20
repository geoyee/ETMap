import os.path as osp
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import GeoExtracter


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    district_id = db.Column(db.Integer, db.ForeignKey("district.id"))
    district = db.relationship("District")

    def __init__(self, id, district, address, lat, lng):
        self.id = id
        self.district = district
        self.address = address
        self.latitude = lat
        self.longitude = lng

    def __repr__(self):
        return "<Point %d: Add. %s Lat %s Lng %s>" % (
            self.id,
            self.address,
            self.latitude,
            self.longitude,
        )


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))

    def __init__(self, id, time):
        self.id = id
        self.time = time


@app.route("/")
def index():
    districts = District.query.all()
    return render_template("index.html", districts=districts)


@app.route("/district/<int:district_id>")
def district(district_id):
    points = Point.query.filter_by(district_id=district_id).all()
    coords = [[point.latitude, point.longitude, point.address] for point in points]
    return jsonify({"data": coords})


def add_datas(path, db):
    geo_extracter = GeoExtracter()
    lnglon_list = geo_extracter.location(path)
    district = District(0, "Time 0")
    db.session.add(district)
    for did, lnglat in enumerate(lnglon_list):
        point = Point(
            did,
            district,
            lnglat["address"],
            lnglat["lat"],
            lnglat["lng"],
        )
        db.session.add(point)
    db.session.commit()


if __name__ == "__main__":
    if not osp.exists("test.db"):
        path = "datas/test.png"
        db.create_all()
        add_datas(path, db)
    app.run(debug=True)
