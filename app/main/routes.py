from flask import render_template, Blueprint, request, redirect, url_for, make_response, flash
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import with_polymorphic

from app import db
from app.models import Member, Artist

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home(username=""):
    # search = SearchForm(request.form)
    # if request.method == 'POST':
    #     return search_results(search)
    if 'username' in request.cookies:
        username = request.cookies.get('username')
    return render_template('home.html', name=username)


@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter a member to search for", "danger")
            return redirect('/')
        results = Member.query.filter(Member.username.contains(term)).all()
        #print(results)
        if not results:
            flash("No member found with that name.", 'danger')
            return redirect('/')
        return render_template('results.html', results=results)
    else:
        return redirect(url_for('main.home'))

#
# @bp_main.route('/results')
# def search_results(search):
#     results = []
#     search_string = search.data['search']
#     if search.data['search'] == '':
#         qry = Member.query()
#         results = qry.all()
#     if not results:
#         flash('No results found!')
#         return redirect('/')
#     else:
#         # display results
#         return render_template('results.html', results=results)


@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.home')))
    response.set_cookie('username', '', expires=datetime.now())
    return response
