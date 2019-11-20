from . import db
import datetime

class UnHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    link = db.Column(db.String(256), unique=True)
    level = db.Column(db.String(10))
    job_network = db.Column(db.String(256))
    job_family = db.Column(db.String(256))
    department = db.Column(db.String(256))
    location = db.Column(db.String(256))
    deadline = db.Column(db.Date())
    update_date = db.Column(db.Date(), default=datetime.datetime.now().date())
    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])

class UnNow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    link = db.Column(db.String(256))
    level = db.Column(db.String(10))
    job_network = db.Column(db.String(256))
    job_family = db.Column(db.String(256))
    department = db.Column(db.String(256))
    location = db.Column(db.String(256))
    deadline = db.Column(db.Date())
    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(256))
    title = db.Column(db.String(256))
    level = db.Column(db.String(10))
    job_network = db.Column(db.String(256))
    job_family = db.Column(db.String(256))
    department = db.Column(db.String(256))
    location = db.Column(db.String(256))

    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])

class UNDataQuery(db.Model):

    def search_by_day(self, col="deadline", star_date=None, end_date=None, today=False):
        if today == True and col=="deadline":
            _date = datetime.datetime.now().date()
            result = db.session.query(UnHistory).filter(UnHistory.deadline == _date).all()
            return result
