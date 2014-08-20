from app import app, db
from flask import render_template, flash, redirect, session, \
    url_for, request, g, jsonify, make_response
from flask.json import dumps
from flask.ext.httpauth import HTTPBasicAuth
from models import Comment, Rest, Badge, User
from forms import RestSearch, SubscribeForm
from helper import get_grade, make_badges, search2, search3, loc_query, getLatestComm, getLatest, dateFrom
from operator import attrgetter, methodcaller
import time
auth = HTTPBasicAuth()
lim = 20 #results page

@app.context_processor
def retWeeks():        
    return dict(weeks=dateFrom)

@auth.get_password
def get_password(username):
    if username == 'foodoo':
        return 'PythonTheGreat'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:pg>/', methods=['GET', 'POST'])
def home(pg=1):
    if 'noloco' in session:
        print 'noloco in sess!'
        session.pop('noloco',none)

    radius = 10
    pg = int(pg)
    offset = pg*20-20
    form = RestSearch()

    if request.args:
        lat = request.args.get('lat', "39.9522")  # city Hall
        lng = request.args.get('lng', "-75.1639")
        try:
            if request.args.get('search', ''):
                term = request.args.get('search', '')
                query = search2(lat, lng, radius, offset, lim, term)
            else:
                query = loc_query(lat, lng, radius, offset, lim)

        except:
            return redirect(url_for('homenoloco'))
        
        rests = Rest.query.from_statement(query).all()

        if not rests:
            print 'redirecting to noloco'
            return redirect(url_for('homenoloco'))

        for rest in rests:
            rest.badges = sorted(make_badges(rest.id))
            try:
                rest.weeks = dateFrom(rest.latestDt())
            except:
                pass
        
        
        return render_template('landing.html', rests=rests,next=pg+1, prev=max(1,pg-1), form=form)

    else:
        # landing inherits from main
        return render_template('landing.html', next=pg+1, prev=max(1,pg-1), form=form)


@app.route('/noloco/<int:pg>', methods=['GET'])
@app.route('/noloco', methods=['GET','POST'])
def homenoloco(pg=1):
    session.noloco = 'y'
    start = time.time()
    offset = pg*20-20
    form = RestSearch()
    if request.args.get('search', ''):
        term = request.args.get('search')
        query = search3(offset, lim, term)
        rests = Rest.query.from_statement(query).all()
    else:
        rests = getLatest(lim,offset)
    
    #resttime = time.time()
    
    for rest in rests:
        #rest.grade = get_grade(rest.getPts())
        rest.badges = sorted(make_badges(rest.id))
    #jrests = [rest.jsond() for rest in rests]
    #landing inherits from main
    
    ### Used to time rest qry and badge making processes ###
    #end = time.time()
    #restqry = resttime-start
    #addbadge = end-resttime
    #print "time it took for rest query is  {} seconds".format(restqry)
    #print "time it took add badges is {} seconds".format(addbadge)
    
    return render_template('landingnoloco2.html', rests=rests, next=pg+1, prev=max(1,pg-1), form=form)


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    rest = Rest.query.get(id)
    form = SubscribeForm()
    othercomments,foodcomments = getLatestComm(id)
    if form.validate_on_submit():
        if not db.session.query(User).\
                filter(User.email == form.data['email']).first():
            u = User(
                form.data['email'],
                form.data['zipcd'],
                form.data['first_name'],
                form.data['last_name'])
            db.session.add(u)
            db.session.commit()
            flash('Thanks for your submission!')
        else:
            flash('Looks like we already have your email on our list!')
    
    return render_template('profile2.html', rest=rest, foodcomments=foodcomments, othercomments=othercomments, form=form)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        if not db.session.query(User).\
                filter(User.email == form.data['email']).first():
            u = User(
                form.data['email'],
                form.data['zipcd'],
                form.data['first_name'],
                form.data['last_name'])
            db.session.add(u)
            db.session.commit()
            flash('Thanks for your submission!')
        else:
            flash('Looks like we already have your email on our list!')
    return render_template('subscribe.html', form=form)

#####################Unused API CODE####################
# @app.route('/api/<int:id>',methods=['GET'])
# @auth.login_required
# def apiProfile(id):
#     profile = Rest.query.get(id)
#     if profile:
#         rest = profile.jsond()
#         rest['badges'] = make_badges(rest['id'])

#         return make_response(jsonify({'profile':rest}))
#     return make_response(jsonify({'Error': 'Page not found'}),404)

# @app.route('/api',methods=['GET'])
# @auth.login_required
# def apiList():
#     ###Query Parameters###
#     lim = request.args.get('limit', 10)
#     off = request.args.get('offset', 0)
#     loc = request.args.get('location', "39.94106,-75.173192")
#     lat, lng = loc.split(",")
#     radius = request.args.get('radius',2)

#     query = loc_query(lat,lng,radius,off,lim)

#     results = Rest.query.from_statement(query).all()

#     rest_json = []
#     rest_json = [rest.jsond() for rest in results]
#     for rest in rest_json:
#         rest['badges'] = make_badges(rest['id'])

#     return make_response(dumps({'count':len(rest_json),'rests':rest_json}))

if __name__ == "__main__":
    api_list2()
