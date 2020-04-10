from . import db
import datetime


# many-to-many tables


user_team = db.Table('user_team',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                      db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'))
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

    # many to many
    teams = db.relationship('Team', secondary=user_team, backref=db.backref('members'),
                            cascade='all, delete'
    )

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.email}) >'


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

    def __repr__(self):
        return f'<Team  {self.name}>'


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

    def __repr__(self):
        return f'<Appraisal by team {self.team_id} ({self.start_date} - {self.end_date})>'


class Review(db.Model):
    """Model for a review."""

    review_id = db.Column(db.Integer, primary_key=True)

    # one to many
    appraisal_id = db.Column(db.Integer, db.ForeignKey('appraisal.appraisal_id'), nullable=False)

    # one to one
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # one to one
    target_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    start_date = db.Column(db.DateTime, default=datetime.datetime.now)

    end_date = db.Column(db.DateTime,
                         index=False,
                         unique=False,
                         nullable=False)

    review_data = db.relationship("ReviewData", uselist=False, backref=db.backref("review"), cascade='delete')

    def __repr__(self):
        return f'<Review {self.review_id} for {self.target_id} by {self.author_id}>'


class ReviewData(db.Model):
    """Model for a review data."""

    review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), primary_key=True)

    review_data = db.Column(db.String(500),
                            index=False,
                            unique=False,
                            nullable=False)

    def __repr__(self):
        return '<Review {}: {}>'.format(self.review_id, self.review_data)

