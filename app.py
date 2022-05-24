from typing import Any
import os.path as osp
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import GeoExtracter
from exts import db
from models import District, Point


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)


@app.route("/")
def index() -> Any:
    districts = District.query.all()
    return render_template("index.html", districts=districts)


@app.route("/district/<int:district_id>")
def district(district_id: int) -> Any:
    points = Point.query.filter_by(district_id=district_id).all()
    coords = [[point.latitude, point.longitude, point.address] for point in points]
    return jsonify({"data": coords})


def add_datas(path: str, city: str, db: SQLAlchemy) -> None:
    geo_extracter = GeoExtracter(city)
    time_dict = geo_extracter.location(path)
    for did, (timer, lnglat_list) in enumerate(time_dict.items()):
        district = District(did, timer)
        db.session.add(district)
        for pid, lnglat in enumerate(lnglat_list):
            point = Point(
                100 * did + pid,
                district,
                lnglat["time"],
                lnglat["address"],
                lnglat["lat"],
                lnglat["lng"],
            )
            db.session.add(point)
    db.session.commit()


if __name__ == "__main__":
    if not osp.exists("app.db"):
        path = "data/test.png"
        with app.app_context():
            db.create_all()
            add_datas(path, "沈阳市", db)
    app.run(debug=True)
