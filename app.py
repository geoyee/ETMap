from typing import Any
import os
import os.path as osp
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
from exts import db
from models import Day, Point, add_datas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index() -> Any:
    if request.method == "POST":
        file = request.files.get("filename")
        if file is not None:
            province = request.form.get("province")  # get province
            city = request.form.get("city")  # get city
            district = province + city if province != city else city
            file_name = file.filename
            file_name = secure_filename(file_name)
            save_dir = osp.join(osp.dirname(__file__), "temp")
            if not osp.exists(save_dir):
                os.makedirs(save_dir)
            save_path = osp.join(save_dir, file_name)
            file.save(save_path)
            with app.app_context():
                add_datas(save_path, district, db)
            days = Day.query.all()
            return render_template("index.html", days=days)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/day/<int:day_id>")
def day(day_id: int) -> Any:
    points = Point.query.filter_by(day_id=day_id).all()
    coords = [[point.latitude, point.longitude, point.address] for point in points]
    return jsonify({"data": coords})


if __name__ == "__main__":
    if osp.exists("app.db"):
        os.remove("app.db")
    with app.app_context():
        db.create_all()
    app.run(debug=True)
