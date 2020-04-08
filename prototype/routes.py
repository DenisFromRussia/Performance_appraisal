from flask import request, make_response
from datetime import datetime as dt

from flask import current_app as app
from prototype.models import db
from prototype.models import User, Team, Appraisal, Review, ReviewData
import json


@app.route('/add_user', methods=['POST'])
def create_user():
    """Add new user to DB."""

    req_dict = json.loads(request.data)
    first_name = req_dict['first_name']
    last_name = req_dict['last_name']
    email = req_dict['email']

    if first_name and last_name and email:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email)

        db.session.add(new_user)
        db.session.commit()
    else:
        return make_response('not valid data received')


    print(User.query.all())

    return make_response(f"{new_user} successfully created!")