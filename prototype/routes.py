from flask import request, make_response
from datetime import datetime as dt

from flask import current_app as app
from prototype.models import db
from prototype.models import User, Team, Appraisal, Review, ReviewData, user_team
from flask import jsonify

# TODO
# Test cascade delete
# Fix adding author and target in Review


# User CRUD

@app.route('/')
@app.route('/user', methods=['POST', 'GET'])
def users():
    """CRUD for users."""
    if request.method == 'GET':
        users = User.query.all()
        return make_response(jsonify(users=[user.serialize() for user in users]))

    elif request.method == 'POST':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        email = request.args.get('email', '')
        role = request.args.get('role', '')
        avatar_url = request.args.get('avatar_url', '')

        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        role=role,
                        avatar_url=avatar_url)

        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(User=new_user.serialize()))


@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    """CRUD for user."""
    if request.method == 'GET':
        new_user = User.query.filter_by(user_id=user_id).one()
        return make_response(jsonify(users=new_user.serialize()))

    elif request.method == 'PUT':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        email = request.args.get('email', '')
        role = request.args.get('role', '')
        avatar_url = request.args.get('avatar_url', '')
        update_user = User.query.filter_by(user_id=user_id).one()

        if first_name:
            update_user.first_name = first_name
        if last_name:
            update_user.last_name = last_name
        if email:
            update_user.email = email
        if role:
            update_user.role = role
        if avatar_url:
            update_user.avatar_url = avatar_url

        db.session.add(update_user)
        db.session.commit()
        return make_response('user with id {} has been updated'.format(user_id))

    elif request.method == 'DELETE':
        delete_user = User.query.filter_by(user_id=user_id).one()
        db.session.delete(delete_user)
        db.session.commit()
        return make_response('user with id {} has been deleted'.format(user_id))


# Team CRUD

@app.route('/team', methods=['POST', 'GET'])
def teams():
    """CRUD for teams."""
    if request.method == 'GET':
        teams = Team.query.all()
        return make_response(jsonify(teams=[team.serialize() for team in teams]))

    elif request.method == 'POST':
        owner_id = request.args.get('owner_id', '')
        if owner_id:
            owner_id = int(owner_id)
            owner = User.query.filter_by(user_id=owner_id).one()
        name = request.args.get('name', '')

        new_team = Team(owner_id=owner,
                        name=name
                        )

        owner.leading_teams.append(new_team)
        db.session.add(new_team)
        db.session.add(owner)
        db.session.commit()
        return make_response(jsonify(Team=new_team.serialize()))


@app.route('/team/<int:team_id>', methods=['GET', 'PUT', 'DELETE'])
def team(team_id):
    """CRUD for team."""
    if request.method == 'GET':
        team = Team.query.filter_by(team_id=team_id).one()
        return make_response(jsonify(teams=team.serialize()))

    elif request.method == 'PUT':
        owner_id = request.args.get('owner_id', '')
        if owner_id:
            owner_id = int(owner_id)
            owner = User.query.filter_by(user_id=owner_id).one()
        name = request.args.get('name', '')
        update_team = User.query.filter_by(team_id=team_id).one()

        if owner_id:
            update_team.owner_id = owner
        if name:
            update_team.name = name

        db.session.add(update_team)
        db.session.commit()
        return make_response('team with id {} has been updated'.format(team_id))

    elif request.method == 'DELETE':
        delete_team = Team.query.filter_by(team_id=team_id).all()[0]
        db.session.delete(delete_team)
        db.session.commit()
        return make_response('team with id {} has been deleted'.format(team_id))


# Appraisal CRUD

@app.route('/appraisal', methods=['POST', 'GET'])
def appraisals():
    """CRUD for appraisals."""
    if request.method == 'GET':
        appraisals = Appraisal.query.all()
        return make_response(jsonify(teams=[appraisal.serialize() for appraisal in appraisals]))

    elif request.method == 'POST':
        team_id = request.args.get('team_id', '')
        if team_id:
            team_id = int(team_id)
            team = Team.query.filter_by(team_id=team_id).one()
        start_date = request.args.get('start_date', '')
        if start_date:
            start_date = dt.strptime(start_date, '%d/%m/%y %H:%M:%S')
        end_date = request.args.get('end_date', '')
        if end_date:
            end_date = dt.strptime(end_date, '%d/%m/%y %H:%M:%S')

        if start_date:
            new_appraisal = Appraisal(
                                      start_date=start_date,
                                      end_date=end_date
                                      )
        else:
            new_appraisal = Appraisal(
                                      end_date=end_date
                                      )
        team.appraisals.append(new_appraisal)
        db.session.add(new_appraisal)
        db.session.add(team)
        db.session.commit()
        return make_response(jsonify(Appraisal=new_appraisal.serialize()))


@app.route('/appraisal/<int:appraisal_id>', methods=['GET', 'PUT', 'DELETE'])
def appraisal(appraisal_id):
    """CRUD for appraisal."""
    if request.method == 'GET':
        appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).one()
        return make_response(jsonify(appraisals=appraisal.serialize()))

    elif request.method == 'PUT':
        team_id = request.args.get('team_id', '')
        if team_id:
            team_id = int(team_id)
            team = Team.query.filter_by(team_id=team_id).one()
        start_date = request.args.get('start_date', '')
        if start_date:
            start_date = dt.strptime(start_date, format='%d/%m/%y %H:%M:%S')
        end_date = request.args.get('end_date', '')
        if end_date:
            end_date = dt.strptime(end_date, format='%d/%m/%y %H:%M:%S')

        update_appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).one()

        if team_id:
            update_appraisal.team_id = team
        if start_date:
            update_appraisal.start_date = start_date
        if end_date:
            update_appraisal.end_date = end_date

        db.session.add(update_appraisal)
        db.session.commit()
        return make_response('appraisal with id {} has been updated'.format(appraisal_id))

    elif request.method == 'DELETE':
        delete_appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).one()
        db.session.delete(delete_appraisal)
        db.session.commit()
        return make_response('appraisal with id {} has been deleted'.format(appraisal_id))

# Review CRUD


@app.route('/review', methods=['POST', 'GET'])
def reviews():
    """CRUD for reviews."""
    if request.method == 'GET':
        reviews = Review.query.all()
        return make_response(jsonify(reviews=[review.serialize() for review in reviews]))

    elif request.method == 'POST':

        appraisal_id = request.args.get('appraisal_id', '')
        if appraisal_id:
            appraisal_id = int(appraisal_id)
            appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).one()

        author_id = request.args.get('author_id', '')
        if author_id:
            author_id = int(author_id)
            author = User.query.filter_by(user_id=author_id).one()

        target_id = request.args.get('target_id', '')
        if target_id:
            target_id = int(target_id)
            target = User.query.filter_by(user_id=target_id).one()

        start_date = request.args.get('start_date', '')
        if start_date:
            start_date = dt.strptime(start_date, '%d/%m/%y %H:%M:%S')

        end_date = request.args.get('end_date', '')
        if end_date:
            end_date = dt.strptime(end_date, '%d/%m/%y %H:%M:%S')

        if start_date:
            new_review = Review(start_date=start_date,
                                end_date=end_date,
                                author_id=author_id,
                                target_id=target_id,
                                appraisal_id=appraisal
                                )
        else:
            new_review = Review(end_date=end_date,
                                author_id=author_id,
                                target_id=target_id,
                                appraisal_id=appraisal
                                )

        print(appraisal.serialize())
        db.session.add(new_review)
        appraisal.reviews.append(new_review)
        db.session.add(appraisal)
        # print(author.serialize())
        # print(new_review.serialize())
        # print(appraisal.serialize())
        db.session.commit()
        return make_response(jsonify(Review=new_review.serialize()))


@app.route('/review/<int:review_id>', methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    """CRUD for review."""
    if request.method == 'GET':
        review = Review.query.filter_by(review_id=review_id).one()
        return make_response(jsonify(reviews=review.serialize()))

    elif request.method == 'PUT':
        appraisal_id = request.args.get('appraisal_id', '')
        if appraisal_id:
            appraisal_id = int(appraisal_id)
            appraisal = Appraisal.query.filter_by(appraisal_id=appraisal_id).one()

        author_id = request.args.get('author_id', '')
        if author_id:
            author_id = int(author_id)
            author = User.query.filter_by(user_id=author_id).one()

        target_id = request.args.get('target_id', '')
        if target_id:
            target_id = int(target_id)
            target = User.query.filter_by(user_id=target_id).one()

        start_date = request.args.get('start_date', '')
        if start_date:
            start_date = dt.strptime(start_date, '%d/%m/%y %H:%M:%S')

        end_date = request.args.get('end_date', '')
        if end_date:
            end_date = dt.strptime(end_date, '%d/%m/%y %H:%M:%S')

        review_data = request.args.get('review_data', '')
        if review_data:
            review_data_obj = ReviewData(review_id=review_id, review_data=review_data)

        update_review = Review.query.filter_by(review_id=review_id).one()

        if start_date:
            update_review.start_date = start_date
        if end_date:
            update_review.end_date = end_date
        if review_data:
            update_review.review_data = review_data_obj

        db.session.add(update_review)
        review_data_obj.review_data = review_data
        db.session.add(review_data_obj)
        # db.session.commit()
        # appraisal.reviews.append(update_review)
        # author.reviews_author.append(update_review)
        # target.reviews_target.append(update_review)
        # db.session.add([appraisal, author, target])
        db.session.commit()

        return make_response('review with id {} has been updated'.format(review_id))

    elif request.method == 'DELETE':
        delete_review = Review.query.filter_by(review_id=review_id).one()
        db.session.delete(delete_review)
        db.session.commit()
        return make_response('review with id {} has been deleted'.format(review_id))
