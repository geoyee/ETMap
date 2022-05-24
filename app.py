from typing import Any
import os.path as osp
from flask import Flask, render_template, jsonify
from exts import db
from models import District, Point, add_datas


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


if __name__ == "__main__":
    if not osp.exists("app.db"):
        path = "data/test.png"
        with app.app_context():
            db.create_all()
            add_datas(path, "沈阳市", db)
    app.run(debug=True)
