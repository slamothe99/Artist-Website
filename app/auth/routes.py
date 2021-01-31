from urllib.parse import urlparse, urljoin
from datetime import timedelta
from flask import Blueprint, flash, make_response, redirect, url_for, render_template, request, abort, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user
from app import db, login_manager, images
from app.auth.forms import SignUpForm, LoginForm
from app.models import Member, Art
from werkzeug.utils import secure_filename
import os

bp_auth = Blueprint('auth', __name__)


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return Member.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.', 'danger')
    return redirect(url_for('auth.log_in'))


@bp_auth.route("/signup/", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        member = Member(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data)
        member.member_type = "member"
        member.set_password(form.password.data)
        try:
            db.session.add(member)
            db.session.commit()
            response = make_response(redirect(url_for('auth.login')))
            response.set_cookie("username", form.username.data)
            flash(f'Account successfully created for {member.username}', 'success')
            return response
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            flash(f'Unable to register {member.username}. Please try again.', 'danger')
    return render_template('signup.html', form=form)


@bp_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Member.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=5))
        flash(f'{user.username} logged in successfully ', 'success')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.home'))
    return render_template('login.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


@bp_auth.route('/gallery/', methods=['GET', 'POST'])
def gallery():
    pics = os.listdir('app/static/images/')
    return render_template('gallery.html', pics=pics)


@bp_auth.route('/events')
def events():
    return render_template('events.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp_auth.route('/artist', methods=['GET', 'POST'])
def artist():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pro-image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pro-image']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('app/static/images/', filename))


        new_file = Art(file_name=filename, genre="any", project_title="test project",
                       collection="any", file_type=".jpg",
                       x_dimension=1, y_dimension=1,
                       file_size="1", resolution=1, data="file.read()")
        db.session.add(new_file)
        db.session.commit()
    return render_template('artist.html')
