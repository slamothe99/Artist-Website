from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class Member(UserMixin, db.Model):
    __tablename__ = 'member'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    member_type = db.Column(db.String(30), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': member_type,
        'polymorphic_identity': 'member'
    }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Member( {self.email}, {self.first_name}, {self.last_name}, {self.username}, {self.password}, {self.biography}, {self.member_type})>"


portfolio_table = db.Table('portfolio', db.Model.metadata,
                           db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
                           db.Column('art_id', db.Integer, db.ForeignKey('art.id')), extend_existing=True)

contributing_artists_table = db.Table('contributing_artists', db.Model.metadata,
                                      db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
                                      db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
                                      extend_existing=True)


class Artist(Member):
    biography = db.Column(db.String(2000))
    num_compositions = db.Column(db.Integer, nullable=False, default=0)
    num_subscribers = db.Column(db.Integer, nullable=False, default=0)
    art = db.relationship("Art", secondary=portfolio_table, backref='artists')
    events = db.relationship("Events", secondary=contributing_artists_table, backref='artists')
    subscriptions = db.relationship("Subscriptions", backref='artist')

    __mapper_args__ = {
        'polymorphic_identity': 'artist'
    }

    def __repr__(self):
        return f"<Artist( {self.artist_id}, {self.num_compositions}, {self.num_subscribers})>"


class Art(db.Model):
    __tablename__ = 'art'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(20))
    project_title = db.Column(db.String(50))
    collection = db.Column(db.String(50))
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    resolution = db.Column(db.Integer)
    x_dimension = db.Column(db.Integer)
    y_dimension = db.Column(db.Integer)
    file_name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"<Art( {self.art_id}, {self.genre}, {self.project_title}, {self.collection}, {self.file_size}, {self.file_type}, {self.resolution}, {self.x_dimension}, {self.y_dimension})>"




class Events(db.Model):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(8), nullable=False)
    end_time = db.Column(db.String(8), nullable=False)
    location = db.Column(db.String(200))
    number_of_compositions = db.Column(db.Integer, nullable=False)
    entry_cost = db.Column(db.Integer, nullable=False)
    number_of_contributing_artists = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Events( {self.event_id}, {self.start_time}, {self.end_time}, {self.location}, {self.number_of_compositions}, {self.entry_cost}, {self.number_of_contributing_artists})>"


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    subscriber_email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Subscriptions( {self.subscription_id}, {self.artist_id}, {self.subscriber_email})>"
