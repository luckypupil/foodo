from app import db
from models import Comment, Rest, Badge
from sqlalchemy import func
import random
from datetime import date, timedelta


def make_badges(restId):
    ### Return unique badge list for restaurant ###
    rest = Rest.query.get(restId)
    badges = []
    for comment in rest.comments.all():
        badge = Badge.query.filter_by(code=comment.code).first()
        if badge and badge.badgenm not in badges:
            badges.append(badge.badgenm)
    return badges

def getVios(restId):
    ### Average violations####
    rest = Rest.query.get(restId)
    vioCtList = db.session.query(func.count(Comment.id)).\
        filter(Comment.restnm == rest.name, Comment.date>(date.today() - timedelta(days=365))).\
        group_by(Comment.date).all() #list of tuples w/ # vios by dates w/in last year        
    
    avgVios = (-1 if len(vioCtList) ==0 else\
                round(sum(float(date[0]) for date in vioCtList)/float(len(vioCtList)),1))#avg of vios from last year.  If none w/in year, '-1' returned
    return avgVios 
    
def getLatest():
    ### returns list of Rest model objects ###
    latestTup = db.session.query(Comment.restnm).\
        group_by(Comment.restnm,Comment.date).order_by(Comment.date.desc()).limit(20).all()
    latestList = [rest[0] for rest in latestTup]
    restList = db.session.query(Rest).filter(Rest.name.in_(latestList)).all()
    
    return restList 
    
def create_badge_list():
    badge_list = {}
    with open('app/badges.csv','r') as badges:
        i = 1
        for line in badges:
            badge_list.setdefault(i,line.encode('utf-8'))
            i+=1
    return badge_list

def make_inspections(restId):
    rest = Rest.query.get(restId)
    inspections = {}
    for comment in rest.comments.all():
        inspections.setdefault(str(comment.date),[]).append(comment.quote)
    return inspections


def loc_query(lat,lng,radius,off,lim):
    
    return("SELECT * FROM (SELECT id, (3959 * acos(cos(radians({latitude})) * cos(radians(lat))\
    * cos(radians(lng) - radians({longitude})) + sin(radians({latitude}))\
    * sin(radians(lat)))) AS distance FROM rest) AS distance WHERE distance\
     < {radius} ORDER BY distance OFFSET {offset} LIMIT {limit};".format(latitude=lat, longitude=lng, radius=radius, offset=off,limit=lim)) 
 
    
# def make_home_api(rest_id):
#     
#     for rest in rest_lst:
#         api = {}
#         sub_dct = {}
#         sub_dct["name"]:rest
        
                
     
# code_to_badge = [    
if __name__ == "__main__":
    getPoints(55381)   
    #loc_query()
