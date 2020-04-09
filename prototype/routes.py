from flask import request, make_response
from datetime import datetime as dt

from flask import current_app as app
from prototype.models import db
from prototype.models import User, Team, Appraisal, Review, ReviewData, user_team
import json


# get user by email
# get all users
# delete user by email
# update user by email


@app.route('/add_user', methods=['POST'])
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
    if len(user) > 1:
        # if the unique feature doesn't works correct
        return make_response(f'sthg is wrong - have {len(user)} users with that email')
    if len(user) == 0:
        return make_response(f'email {email} doesnt belong to any user')
    # list of one element
    user = user[0]
    db.session.delete(user)
    db.session.commit()
    return make_response('succesfully deleted')
        



@app.route('/update_user', methods=['POST'])
def update_user():
    """Update user info."""

    req_dict = json.loads(request.data)     
    email = req_dict.pop('email', None)
    if not email:
        return make_response('No email given')

    user = User.query.filter_by(email=email).all()
    if len(user) > 1:
        return make_response(f'sthg is wrong - have {len(user)} users with that email')
    if len(user) == 0:
        return make_response(f'no user with  email {email}')
    # only this way: user[0].update(...) doesn't work
    User.query.filter_by(email=email).update(req_dict)
    db.session.commit()
    return make_response('Succesfully updated')


@app.route('/show_all_users', methods=['POST'])
def show_all_users():
    """Show all users."""

    users = User.query.all()
    # return emails
    response = ", ".join([user.email for user in users])
    return make_response(response)


@app.route('/get_user', methods=['POST'])
def get_user():
    """Get user info from DB by email."""
    req_dict = json.loads(request.data)
    email = req_dict['email'].lower()

    user = User.query.filter_by(email=email).all()
    if len(user) > 1:
        # if the unique feature doesn't works correct
        return make_response(f'sthg is wrong - have {len(user)} users with that email')
    if len(user) == 0:
        return make_response('this email doesnt belong to any user')
    # list of one element
    user = user[0]
    print(user)
    # return make_response(f'user info: \n {user}')
    return make_response(f'user info: \n {user.__dict__}')