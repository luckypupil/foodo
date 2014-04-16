from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g 
from models import Comment, Rest
from forms import HomeSearch
from helper import make_badges

@app.route('/')
def home():
    rests = Rest.query.all()
    scores = {}
    for rest in rests:
        scores[rest.id] = make_badges(rest.id)    

    return render_template('main.html',rests = rests, scores = scores)

@app.route('/profile/<nameslug>')
def profile(nameslug):
    restuarant = Rest.query.get(35)  
    name = restuarant.name_slug() 
    return render_template('profile.html',name = name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    