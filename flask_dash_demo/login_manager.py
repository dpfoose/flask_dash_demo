import os
from flask_login import LoginManager, login_required
from db_models import User

login_manager = LoginManager()

login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return
    return user


def authenticate_user(req):
    email = req.form.get('email')
    password = req.form.get('password')
    if email is None and password is None:
        req_json = req.get_json(force=True)
        email = req_json['username']
        password = req_json['password']
    user = User.query.filter_by(email=email).first()
    print(password)
    print(email)
    print(User.query.all())
    if user is not None and user.check_password(password):
        return user
    raise ValueError('Incorrect username/password.')
