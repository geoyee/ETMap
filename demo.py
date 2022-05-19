from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude_off = db.Column(db.Float)
    longitude_off = db.Column(db.Float)
    district_id = db.Column(db.Integer, db.ForeignKey("district.id"))
    district = db.relationship("District")

    def __init__(self, id, district, lat, lng):
        self.id = id
        self.district = district
        self.latitude_off = lat
        self.longitude_off = lng

    def __repr__(self):
        return "<Point %d: Lat %s Lng %s>" % (
            self.id,
            self.latitude_off,
            self.longitude_off,
        )

    @property
    def latitude(self):
        return self.latitude_off + self.district.latitude

    @property
    def longitude(self):
        return self.longitude_off + self.district.longitude


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, id, name, lat, lng):
        self.id = id
        self.name = name
        self.latitude = lat
        self.longitude = lng


@app.route("/")
def index():
    districts = District.query.all()
    return render_template("index.html", districts=districts)


@app.route("/district/<int:district_id>")
def district(district_id):
    points = Point.query.filter_by(district_id=district_id).all()
    coords = [[point.latitude, point.longitude] for point in points]
    return jsonify({"data": coords})


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
