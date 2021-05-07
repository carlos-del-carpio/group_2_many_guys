from database import db
import datetime


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    event_title = db.Column("event_title", db.String(200))
    event_description = db.Column("event_text", db.String(100))
    event_date = db.Column("event_date", db.String(50))
    event_creator = db.Column("event_creator", db.String(100))
    date_created = db.Column("date_created", db.String(50))
    # can create a foreign key; referencing the id variable in the User class
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="event", cascade="all, delete-orphan", lazy=True)
    like = db.Column("like", db.String(200))
    dislike = db.Column("dislike", db.String(200))
    count = db.Column("count", db.Integer)
    
    def __init__(self, title, description, date, creator, user_id, date_created):
        self.event_title = title
        self.event_description = description
        self.event_date = date
        self.event_creator = creator
        self.date_created = date_created
        self.user_id = user_id
        self.like = "|"
        self.dislike = "|"
        self.count = 0


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    full_name = db.Column("full_name", db.String(200))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    event = db.relationship("Event", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, event_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.event_id = event_id
        self.user_id = user_id
