from flask_sqlalchemy import SQLAlchemy
from utils import GeoExtracter
from exts import db


class Day(db.Model):
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
    day_id = db.Column(db.Integer, db.ForeignKey("day.id"))
    day = db.relationship("Day")

    def __init__(
        self,
        id: int,
        day: Day,
        time: str,
        address: str,
        lat: float,
        lng: float,
    ) -> None:
        self.id = id
        self.day = day
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
        day = Day(did, timer)
        db.session.add(day)
        for pid, lnglat in enumerate(lnglat_list):
            point = Point(
                100 * did + pid,
                day,
                lnglat["time"],
                lnglat["address"],
                lnglat["lat"],
                lnglat["lng"],
            )
            db.session.add(point)
    db.session.commit()
