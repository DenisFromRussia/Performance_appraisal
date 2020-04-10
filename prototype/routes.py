from flask import request, make_response
from datetime import datetime as dt

from flask import current_app as app
from prototype.models import db
from prototype.models import User, Team, Appraisal, Review, ReviewData, user_team
from flask import jsonify
import json


# User CRUD

@app.route('/create_user', methods=['POST'])
def create_user():
    """Add new user to DB."""

    req_dict = json.loads(request.data)
    first_name = req_dict['first_name'].lower()
    last_name = req_dict['last_name'].lower()
    email = req_dict['email'].lower()
    role = req_dict['role'].lower()
    avatar_url = req_dict['avatar_url'].lower()

    if not (first_name and last_name and email):
        return make_response('not enough data')

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role=role,
                    avatar_url=avatar_url)

    db.session.add(new_user)
    db.session.commit()

    # test if by deleting a user team will also deleted
    user = User.query.all()[-1]
    user.teams = [
        Team(owner_id=new_user.user_id,
            name=f'ДБД_{email}'
            ),
        Team(owner_id=new_user.user_id,
            name=f'ДБСАПА_{email}'
            )
    ]
    db.session.commit()
    print("teams; ", Team.query.all())

    return make_response(f"{new_user} successfully created!")


@app.route('/delete_user', methods=['POST'])
def delete_user():
    """Delete user from DB by email."""

    req_dict = json.loads(request.data)
    email = req_dict['email'].lower()

    user = User.query.filter_by(email=email).all()

    if len(user) == 0:
        return make_response(f'no user with email {email}')

    # list of one element
    user = user[0]
    db.session.delete(user)
    db.session.commit()
    return make_response(f'{email} successfully deleted')
        

@app.route('/update_user', methods=['POST'])
def update_user():
    """Update user info."""

    req_dict = json.loads(request.data)     
    email = req_dict.pop('email', None)
    if not email:
        return make_response('No email given')

    user = User.query.filter_by(email=email).all()

    if len(user) == 0:
        return make_response(f'no user with email {email}')

    # only this way: user[0].update(...) doesn't work
    User.query.filter_by(email=email).update(req_dict)
    db.session.commit()

    return make_response(f'{email} successfully updated')


@app.route('/get_all_users', methods=['POST'])
def get_all_users():
    """Return all users."""

    users = User.query.all()
    # return emails
    response = [user.__repr__() for user in users]
    return make_response(jsonify(response))


@app.route('/get_user', methods=['POST'])
def get_user():
    """Get user info from DB by email."""
    req_dict = json.loads(request.data)
    email = req_dict['email'].lower()

    user = User.query.filter_by(email=email).all()
    if len(user) == 0:
        return make_response(f'no user with email {email}')
    # list of one element
    user = user[0]
    user_dict = user.__dict__

    del user_dict['_sa_instance_state']

    return make_response(jsonify(user_dict))


# TODO function to add a user to a given team

# Team CRUD

@app.route('/create_team', methods=['POST'])
def create_team():
    """Add new team to DB."""

    req_dict = json.loads(request.data)

    # TODO get owner's email in request and find owner_id in backend
    owner_id = int(req_dict['owner_id'])
    name = req_dict['name']

    if not (owner_id and name):
        return make_response('not enough data')

    new_team = Team(owner_id=owner_id, name=name)

    db.session.add(new_team)
    db.session.commit()

    return make_response(f"{new_team} team successfully created!")


@app.route('/delete_team', methods=['POST'])
def delete_team():
    """Delete team from DB its name."""

    req_dict = json.loads(request.data)

    name = req_dict['name']

    team = Team.query.filter_by(name=name).all()

    if len(team) == 0:
        return make_response(f'name {name} doesnt belong to any team')
    # list of one element
    team = team[0]
    db.session.delete(team)
    db.session.commit()
    return make_response(f'{name} team has been deleted')


@app.route('/update_team', methods=['POST'])
def update_team():
    """Update team info."""

    req_dict = json.loads(request.data)
    name = req_dict.pop('name', None)

    if not name:
        return make_response('no name given')

    team = Team.query.filter_by(name=name).all()

    if len(team) == 0:
        return make_response(f'name {name} doesnt belong to any team')

    Team.query.filter_by(name=name).update(req_dict)
    db.session.commit()

    return make_response(f'team {name} successfully updated')


@app.route('/get_all_teams', methods=['POST'])
def get_all_teams():
    """Return all teams."""

    teams = Team.query.all()

    # return team names
    response = [team.__repr__() for team in teams]
    return make_response(jsonify(response))


@app.route('/get_team', methods=['POST'])
def get_team():
    """Get team info from DB by its name."""

    req_dict = json.loads(request.data)
    name = req_dict['name']

    team = Team.query.filter_by(name=name).all()

    if len(team) == 0:
        return make_response('this name doesnt belong to any team')
    # list of one element
    team = team[0]
    team_dict = team.__dict__
    del team_dict['_sa_instance_state']

    # add number of members
    if 'members' in team_dict:
        team_dict['size'] = len(team_dict['members'])
    else:
        team_dict['size'] = 0

    print(team_dict)

    return make_response(jsonify(team_dict))


# Appraisal CRUD

@app.route('/create_appraisal', methods=['POST'])
def create_appraisal():
    """Add new appraisal to DB."""

    req_dict = json.loads(request.data)

    # TODO get team's name in request and find team_id in backend
    team_id = int(req_dict['team_id'])
    name = req_dict['name']
    end_time = dt.strptime(req_dict['end_time'], format='%d/%m/%y %H:%M:%S')

    if not (team_id and name and end_time):
        return make_response('not enough data')

    new_appraisal = Appraisal(team_id=team_id, name=name, end_time=end_time)

    db.session.add(new_appraisal)
    db.session.commit()

    return make_response(f"{new_appraisal} appraisal has been created!")


@app.route('/delete_appraisal', methods=['POST'])
def delete_appraisal():
    """Delete appraisal from DB by its id."""

    req_dict = json.loads(request.data)

    appraisal_id = int(req_dict['appraisal_id'])

    appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).all()

    # list of one element
    appraisal = appraisal[0]
    db.session.delete(appraisal)
    db.session.commit()
    return make_response(f'{appraisal} has been deleted')


@app.route('/update_appraisal', methods=['POST'])
def update_appraisal():
    """Update appraisal info by its id."""

    req_dict = json.loads(request.data)

    appraisal_id = req_dict.pop('appraisal_id', None)

    if not appraisal_id:
        return make_response('No appraisal id given')

    Appraisal.query.filter_by(appraisal_id=appraisal_id).update(req_dict)
    db.session.commit()

    return make_response('successfully updated')


@app.route('/get_all_appraisals', methods=['POST'])
def get_all_appraisals():
    """Return all appraisals."""

    appraisals = Appraisal.query.all()

    # return a list of all appraisals
    response = [appraisal.__repr__() for appraisal in appraisals]
    return make_response(jsonify(response))


@app.route('/get_appraisal', methods=['POST'])
def get_appraisal():
    """Get appraisal info from DB by its id."""

    req_dict = json.loads(request.data)
    appraisal_id = req_dict['appraisal_id']
    appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).all()
    appraisal_dict = appraisal[0].__dict__

    del appraisal_dict['_sa_instance_state']

    # add number of reviews
    appraisal_dict['number_of_reviews'] = len(appraisal_dict['reviews'])

    print(appraisal_dict)

    return make_response(jsonify(appraisal_dict))


# Review (and ReviewData) CRUD

@app.route('/create_review', methods=['POST'])
def create_review():
    """Add new review to DB."""

    req_dict = json.loads(request.data)

    # TODO get author's and target's emails in request and find author_id and target_id in backend
    author_id = int(req_dict['author_id'])
    target_id = int(req_dict['target_id'])
    end_date = dt.strptime(req_dict['end_date'], format='%d/%m/%y %H:%M:%S')

    if not (author_id and target_id and end_date):
        return make_response('not enough data')

    new_review = Review(author_id=author_id, target_id=target_id, end_date=end_date)

    db.session.add(new_review)
    db.session.commit()

    return make_response(f"{new_review} review has been created!")


@app.route('/create_review_data', methods=['POST'])
def create_review_data():
    """Create review data."""

    req_dict = json.loads(request.data)
    review_id = req_dict['review_id']
    review_data = req_dict['review_data']

    if not review_data:
        return make_response('no review data given')

    new_review_data = ReviewData(review_id=review_id, review_data=review_data)
    db.session.add(new_review_data)
    db.session.commit()

    return 'review data was successfully created'


@app.route('/delete_review', methods=['POST'])
def delete_review():
    """Delete review from DB by its id."""

    req_dict = json.loads(request.data)

    review_id = int(req_dict['review_id'])

    review = Review.query.filter_by(review_id=review_id).all()

    # list of one element
    review = review[0]
    db.session.delete(review)
    db.session.commit()
    return make_response(f'{review} has been deleted')


@app.route('/update_review', methods=['POST'])
def update_review():
    """Update review info by its id."""

    req_dict = json.loads(request.data)

    review_id = req_dict.pop('review_id', None)

    if not review_id:
        return make_response('No review id given')

    Review.query.filter_by(review_id=review_id).update(req_dict)
    db.session.commit()

    return make_response('successfully updated')


@app.route('/get_all_reviews', methods=['POST'])
def get_all_reviews():
    """Return all reviews."""

    reviews = Review.query.all()

    # return a list of all reviews
    response = [review.__repr__() for review in reviews]
    return make_response(jsonify(response))


@app.route('/get_review', methods=['POST'])
def get_review():
    """Get review info from DB by its id."""

    req_dict = json.loads(request.data)
    review_id = req_dict['review_id']
    review = Review.query.filter_by(review_id=review_id).all()
    review_dict = review[0].__dict__

    del review_dict['_sa_instance_state']

    # get review data
    review_data = ReviewData.query.filter_by(review_id=review_id).all()
    review_data = review_data[0]

    # add review data to review dict
    review_dict['review_data'] = review_data

    print(review_dict)

    return make_response(jsonify(review_dict))


# get all user-team table

# @app.route('/get_all_user_team_connection', methods=['POST'])
# def get_all_user_team_connection():
#     """Return all user-teams connections."""
#
#     users_team_connections = user_team.query.all()
#     # return user-team connections
#     return make_response(jsonify(users_team_connections))
