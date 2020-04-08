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
    first_name = req_dict['first_name']
    last_name = req_dict['last_name']
    email = req_dict['email']
    role = req_dict['role']
    avatar_url = req_dict['avatar_url']

    if first_name and last_name and email:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        role=role,
                        avatar_url=avatar_url)

        db.session.add(new_user)
        db.session.commit()
    else:
        return make_response('not valid data received')


    # print(User.query.all())
    # print(Team.query.all())
    # print(Appraisal.query.all())
    # print(Review.query.all())
    # print(ReviewData.query.all())

    # user = User.query.all()[-1]
    # user.teams = [
    #     Team(owner_id=new_user.user_id,
    #          name='ДБД',
    #
    #          ),
    #     Team(owner_id=new_user.user_id,
    #          name='ДБСАПА'
    #          )
    # ]
    # db.session.commit()


    return make_response(f"{new_user} successfully created!")