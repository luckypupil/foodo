from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response
from flask.json import dumps
from flask.ext import restful 
from flask.ext.httpauth import HTTPBasicAuth
from models import Comment, Rest, Badge
from forms import HomeSearch
from helper import make_badges, make_inspections, loc_query, getVios, getLatest
from operator import attrgetter
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'foodoo':
        return 'PythonTheGreat'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}), 401)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/latest')
def home():
    rests = getLatest(5)
    jrests = [rest.jsond() for rest in rests]  
    return render_template('webflow.html',rests = rests, jrests=jrests)

@app.route('/points')
def homePoints():
    rests = Rest.query.limit(10).all()
    for rest in rests:
        rest.score = getVios(rest.id) 
    rests = sorted(rests,key=attrgetter('score'),reverse=True) 
    return render_template('main.html',rests = rests)

@app.route('/proximity')
def homeProximity():
    lim = request.args.get('limit', 10)
    off = request.args.get('offset', 1)
    loc = request.args.get('location', "39.941063, -75.173192")
    lat, lng = loc.split(",")
    radius = request.args.get('radius',2)
    query = loc_query(lat,lng,radius,off,lim)
    rests = Rest.query.from_statement(query).all()
    jrests = [rest.jsond() for rest in rests]  
    return render_template('mainWithMap.html',rests = rests, jrests=jrests)

@app.route('/profile/<int:id>')
def profile(id):
    rest = Rest.query.get(id)  
    restProfile = rest.jsond()
    badges = make_badges(rest.id) 
    latest = getVios(rest.id)
    return render_template('profile.html',rest = restProfile,badges=badges, latest=latest)

@app.route('/api/<int:id>',methods=['GET'])
@auth.login_required
def apiProfile(id):
    profile = Rest.query.get(id)
    if profile:
        rest = profile.jsond()
        rest['badges'] = make_badges(rest['id'])
        
        return make_response(jsonify({'profile':rest}))
    return make_response(jsonify({'Error': 'Page not found'}),404)

@app.route('/api',methods=['GET'])
@auth.login_required
def apiList():
    ###Query Parameters###
    lim = request.args.get('limit', 10)
    off = request.args.get('offset', 0)
    loc = request.args.get('location', "39.94106,-75.173192")
    lat, lng = loc.split(",")
    radius = request.args.get('radius',2)
    
    query = loc_query(lat,lng,radius,off,lim)
        
    results = Rest.query.from_statement(query).all()
    
    rest_json = []
    rest_json = [rest.jsond() for rest in results]
    for rest in rest_json:
        rest['badges'] = make_badges(rest['id'])
    
    return make_response(dumps({'count':len(rest_json),'rests':rest_json}))

if __name__ == "__main__":
    api_list2()    
