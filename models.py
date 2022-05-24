from flask_sqlalchemy import SQLAlchemy
from utils import GeoExtracter
from exts import db


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10))

    def __init__(self, id: int, time: str) -> None:
        self.id = id
        self.time = time


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10))
    address = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    district_id = db.Column(db.Integer, db.ForeignKey("district.id"))
    district = db.relationship("District")

    def __init__(
        self,
        id: int,
        district: District,
        time: str,
        address: str,
        lat: float,
        lng: float,
    ) -> None:
        self.id = id
        self.district = district
        self.time = time
        self.address = address
        self.latitude = lat
        self.longitude = lng

    def __repr__(self) -> str:
        return "<Point %d: Add. %s Lat %s Lng %s>" % (
            self.id,
            self.address,
            self.latitude,
            self.longitude,
        )


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
