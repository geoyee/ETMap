from typing import Any
import os
import os.path as osp
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
from exts import db
from models import District, Point, add_datas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index() -> Any:
    if request.method == "POST":
        file = request.files.get("filename")
        if file is not None:
            province = request.form.get("province")  # get province
            file_name = file.filename
            file_name = secure_filename(file_name)
            save_dir = osp.join(osp.dirname(__file__), "temp")
            if not osp.exists(save_dir):
                os.makedirs(save_dir)
            save_path = osp.join(save_dir, file_name)
            file.save(save_path)
            with app.app_context():
                db.create_all()
                add_datas(save_path, province, db)
            districts = District.query.all()
            return render_template("index.html", districts=districts)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/district/<int:district_id>")
def district(district_id: int) -> Any:
    points = Point.query.filter_by(district_id=district_id).all()
    coords = [[point.latitude, point.longitude, point.address] for point in points]
    return jsonify({"data": coords})


if __name__ == "__main__":
    app.run(debug=True)
