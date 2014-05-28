from app import app, db, admin
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response
from flask.json import dumps
from flask.ext import restful 
from flask.ext.httpauth import HTTPBasicAuth
from models import Comment, Rest, Badge
from forms import addySearch
from helper import *
from operator import attrgetter, methodcaller
from flask.ext.admin.contrib.sqla import ModelView
from pprint import pprint
auth = HTTPBasicAuth()

admin.add_view(ModelView(Rest, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Badge, db.session))

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

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

# @app.route('/science',methods=['GET'])
# def about():
#     return render_template('science.html')
lim = 30


@app.route('/',methods=['GET', 'POST'])
def home():
    radius = 5
    form = addySearch()
    if form.validate_on_submit():
        return 'form validated'
        #Do code  
    if request.args:
        sortOpts = ['viosLow','viosHigh','date']
        lat = request.args.get('lat', "39.9522")#city Hall
        lng = request.args.get('lng', "-75.1639")
        sort = request.args.get('sort',sortOpts[0])#'vios' needs to be specified if sort desired
        try:
            query = loc_query(lat,lng,radius,lim)
        except:
            return redirect(url_for('homenoloco'))

        rests = Rest.query.from_statement(query).all()
        for rest in rests:
            rest.badges = sorted(make_badges(rest.id)) 
        if sort == sortOpts[1]:#Highest vios 1st
            rests = sorted(rests,key=methodcaller('getVios'),reverse=True)
        elif sort == sortOpts[2]:#Recent date first
            rests = sortRestLatest(rests)
        else:
            rests = sorted((rest for rest in rests if rest.getVios()>=0),key=methodcaller('getVios'))        

        #jrests = [rest.jsond() for rest in Rest.query.all()] #Eventually will load full data in background      
        return render_template('landing.html',rests = rests, form = form)
        
    else:
        return render_template('landing.html')#landing inherits from main

@app.route('/noloco',methods=['GET'])
def homenoloco():
    form = addySearch()
    rests = getLatest(lim)
    for rest in rests:
        rest.score = getVios(rest.id)
        rest.badges = sorted(make_badges(rest.id))
        
    jrests = [rest.jsond() for rest in rests]  
    return render_template('landingnoloco.html',rests = rests, jrests=jrests, form = form)#landing inherits from main



@app.route('/profile/<int:id>')
def profile(id):
    rest = Rest.query.get(id)  
    comments = getLatestComm(id)
    return render_template('profile.html', rest = rest,comments=comments)

##################################Unused API CODE##################################################
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
