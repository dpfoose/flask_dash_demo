import traceback

from flask import Flask, url_for, redirect, render_template, request
from flask_login import login_required, current_user, login_user, logout_user

from dashboards import dashboard_list
from login_manager import login_manager, authenticate_user
from db_models import User, Wine, db
from dummy_data import create_dummy_user, load_wine_data

app = Flask(__name__)
app.secret_key = 'SuperDuperSecretSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///./app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
    db.init_app(app)
    db.create_all()
    if User.query.first() is None:
        create_dummy_user()
    if Wine.query.first() is None:
        load_wine_data()

    for app_type in dashboard_list:
        try:
            app_type.create_dash_app(app)
        except:
            traceback.print_exc()

    for view_func in app.view_functions:
        if view_func.startswith('/dashboards'):
            app.view_functions[view_func] = login_required(app.view_functions[view_func])

    login_manager.init_app(app)


app.jinja_env.globals.update(url_for=url_for)
app.jinja_env.globals.update(current_user=current_user)


@app.route('/')
def render_root():
    return redirect(url_for('render_home'))


@app.route('/login', methods=['GET', 'POST'])
def login(msg=None, error=None):
    try:
        if request.method == 'POST':
            redirect_url = request.args.get('next') if request.args.get('next') is not None \
                else url_for('render_home')
            user = authenticate_user(request)
            login_user(user)
            return redirect(redirect_url)
    except ValueError as e:
        return render_template('login.html', error=str(e))
    return render_template('login.html', msg=msg, error=error)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def render_home():
    return render_template('home.html')


@app.route('/dashboards')
@login_required
def render_dashboard_list():
    return render_template('dashboard_list.html', dashboards=dashboard_list, active_nav_item='dashboard-link')


@app.route('/wines')
@login_required
def render_wine_list():
    return render_template('wine_list.html', wines=Wine.query.all(), active_nav_item='wine-link')


@app.route('/wines/<wine_id>')
@login_required
def render_wine_entry(wine_id):
    wine = Wine.query.filter_by(id=wine_id).first()
    return render_template('wine_entry.html', wine=wine, active_nav_item='wine-link')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
