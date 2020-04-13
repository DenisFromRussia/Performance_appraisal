from . import db
import datetime


# many-to-many tables


user_team = db.Table('user_team',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
                      db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
                      )

# entity tables


class User(db.Model):
    """Model for a user accounts."""

    user_id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64),
                         index=False,
                         unique=False,
                         nullable=False)

    last_name = db.Column(db.String(64),
                         index=False,
                         unique=False,
                         nullable=False)

    email = db.Column(db.String(80),
                      index=False,
                      unique=True,
                      nullable=False)

    avatar_url = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)

    role = db.Column(db.String(64),
                       index=False,
                       unique=False,
                       nullable=False)

    leading_teams = db.relationship('Team', backref='owner')

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'leading_teams': [i.__repr__() for i in self.leading_teams]
        }

    # many to many
    # teams = db.relationship('Team', secondary=user_team, backref=db.backref('members'),
    #                         cascade='all, delete'
    # )

    def __repr__(self):
        return str(self.user_id)


class Team(db.Model):
    """Model for a team."""

    team_id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    name = db.Column(db.String(64),
                          index=False,
                          unique=True,
                          nullable=False)

    # one to many
    appraisals = db.relationship('Appraisal', backref='team')

    members = db.relationship("User", cascade="all,delete", backref=db.backref("Team"), secondary=user_team)

    def serialize(self):
        return {
            'team_id': self.team_id,
            'owner_id': self.owner_id,
            'name': self.name,
            'appraisals': [i.__repr__() for i in self.appraisals],
            'members': [i.__repr__() for i in self.members],
            'size': len(self.members)
        }

    def __repr__(self):
        return str(self.team_id)


class Appraisal(db.Model):
    """Model for a appraisal."""

    appraisal_id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)

    start_date = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           index=False,
                           unique=False,
                           nullable=False
                           )

    end_date = db.Column(db.DateTime,
                            index=False,
                            unique=False,
                            nullable=False
                             )

    reviews = db.relationship('Review', backref='appraisal')

    def serialize(self):
        return {
            'appraisal_id': self.appraisal_id,
            'team_id': self.team_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'reviews': [int(i.__repr__()) for i in self.reviews],
            'number_of_reviews': len(self.reviews)
        }

    def __repr__(self):
        return str(self.appraisal_id)


class Review(db.Model):
    """Model for a review."""

    review_id = db.Column(db.Integer, primary_key=True)

    # one to many
    appraisal_id = db.Column(db.Integer, db.ForeignKey('appraisal.appraisal_id'), nullable=False)
    author_id = db.Column(db.Integer, nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    # one to one
    # author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # one to one
    # target_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # author = db.relationship("User", backref=db.backref('review_author', uselist=True), foreign_keys=[author_id])
    # target = db.relationship("User", backref=db.backref('review_target', uselist=True), foreign_keys=[target_id])

    start_date = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           index=False,
                           unique=False,
                           nullable=False
                           )

    end_date = db.Column(db.DateTime,
                         index=False,
                         unique=False,
                         nullable=False)

    review_data = db.relationship("ReviewData", uselist=False, backref=db.backref("review"), cascade='delete')

    def serialize(self):
        return {
            'review_id': self.review_id,
            'appraisal_id': int(self.appraisal_id.__repr__()),
            'author_id': int(self.author_id.__repr__()),
            'target_id': int(self.target_id.__repr__()),
            'start_date': self.start_date,
            'end_date': self.end_date,
            'review_data': self.review_data.__repr__()
        }

    def __repr__(self):
        return str(self.review_id)


class ReviewData(db.Model):
    """Model for a review data."""

    review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), primary_key=True)

    review_data = db.Column(db.String(500),
                            index=False,
                            unique=False,
                            nullable=False)

    def serialize(self):
        return {
            'review_id': self.review_id,
            'review_data': self.review_data,
        }

    def __repr__(self):
        return str(self.review_data)

