from . import db


# many-to-many tables


staff_team = db.Table('user_team', db.metadata,
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

    # one to many
    teams = db.relationship('Team', backref='member')

    # one to one
    review_authorities = db.relationship('Review', db.ForeignKey('User.user_id'))
    review_targets = db.relationship('Review', db.ForeignKey('User.user_id'))

    # many to many
    team = db.relationship('Team', secondary=staff_team, backref=db.backref('members', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.email})>'


class Team(db.Model):
    """Model for a team."""

    team_id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    name = db.Column(db.String(64),
                          index=False,
                          unique=False,
                          nullable=False)

    appraisals = db.relationship('Appraisal', backref='team', lazy=True)

    def __repr__(self):
        return f'<Team  {self.name}>'


class Appraisal(db.Model):
    """Model for a appraisal."""

    appraisal_id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)

    start_date = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)

    end_date = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)

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

    start_date = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=False)

    end_date = db.Column(db.DateTime,
                         index=False,
                         unique=False,
                         nullable=False)

    review_data = db.relationship("ReviewData", uselist=False, back_populates="parent")

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

