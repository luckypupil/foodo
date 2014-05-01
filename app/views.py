from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response
from flask.ext import restful 
from flask.ext.httpauth import HTTPBasicAuth
from models import Comment, Rest, Badge
from forms import HomeSearch
from helper import make_badges, make_inspections, loc_query
import operator
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'foodoo':
        return 'PythonTheGreat'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}), 401)


@app.route('/')
def home():
  
    lim = request.args.get('limit', 20)
    off = request.args.get('offset', 0)
    loc = request.args.get('location', "39.9800,-75.23192")
    lat, lng = loc.split(",")
    radius = request.args.get('radius',2)
    
    query = loc_query(lat,lng,radius,off,lim)
    rests = Rest.query.from_statement(query).all()
    scores = {}
    for rest in rests:
        scores[rest.id] = make_badges(rest.id)    
        
    return render_template('main.html',rests = rests, scores = scores)

@app.route('/profile/<int:id>')
def profile(id):
    restuarant = Rest.query.get(id)  
    name = restuarant.name_slug() 
    return render_template('profile.html',name = name)

@app.route('/api/<int:id>',methods=['GET'])
@auth.login_required
def api_profile(id):
    profile = Rest.query.get(id)
    if profile:
        json_obj = {
            'id': profile.id,
            'name': profile.name,
            'steet': profile.street,
            'zipcd': profile.zipcd,
            'badges': make_badges(profile.id),
            'inspection' : make_inspections(profile.id)
            }
        
        return make_response(jsonify({'profile':json_obj}))
    return make_response(jsonify({'Error': 'Page not found'}),404)

@app.route('/api',methods=['GET'])
@auth.login_required
def api_list():
    ###Query Parameters###
    lim = request.args.get('limit', 10)
    off = request.args.get('offset', 0)
    loc = request.args.get('location', "39.94106,-75.173192")
    lat, lng = loc.split(",")
    radius = request.args.get('radius',2)
    
    query = loc_query(lat,lng,radius,off,lim)
        
    results = Rest.query.from_statement(query).all()
    
    rest_json = []
    for rest in results:
        json_obj = {
            'id': rest.id,
            'name': rest.name,
            'steet': rest.street,
            'zipcd': rest.zipcd,
            'badges': make_badges(rest.id),
            'lat': rest.lat,
            'lng': rest.lng,
            }
        rest_json.append(json_obj)
         
        
    return make_response(jsonify({'count':len(rest_json),'rests':rest_json}))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    