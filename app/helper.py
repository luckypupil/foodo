from app import db
from models import Comment, Rest, Badge
from sqlalchemy import func
import random
from datetime import date, timedelta
from operator import methodcaller


def make_badges(restId):
    ### Return unique badge list for restaurant ###
    rest = Rest.query.get(restId)
    latestCommentsTup = db.session.query(Comment.code).filter(rest.latestDt()==Comment.date,rest.name==Comment.restnm).all()
    latestComments = [comment[0] for comment in latestCommentsTup]
    badges = []
    for code in latestComments:
        badge = db.session.query(Badge).filter(Badge.code==code).first()
        if badge and badge.badgenm not in badges:
            badges.append(badge.badgenm)
    return badges

def getLatestComm(restId):
    #List of comments from rest's most recent inspection#
    rest = Rest.query.get(restId)
    ltDt = rest.latestDt()
    latComm = db.session.query(Comment.quote).filter(Comment.restnm == rest.name,Comment.date == ltDt).all()
    return [str(comm).decode('utf8').strip("(u'").strip("',)") for comm in latComm]
def getVios(restId):
    ### Average violations####
    rest = Rest.query.get(restId)
    vioCtList = db.session.query(func.count(Comment.id)).\
        filter(Comment.restnm == rest.name, Comment.date>(date.today() - timedelta(days=365))).\
        group_by(Comment.date).all() #list of tuples w/ # vios by dates w/in last year        
    
    avgVios = (-1 if len(vioCtList) ==0 else\
                round(sum(float(date[0]) for date in vioCtList)/float(len(vioCtList)),1))#avg of vios from last year.  If none w/in year, '-1' returned
    return avgVios 

def sortRestLatest(restList):
    sortLst = sorted(restList,key=methodcaller('latestDt'),reverse=True)
    return sortLst 

def getLatest(limit=20):
    ### returns list of Rest model objects ###
    latestTup = db.session.query(Comment.restnm).\
        group_by(Comment.restnm,Comment.date).order_by(Comment.date.desc()).limit(limit).all()
    latestList = [rest[0] for rest in latestTup]
    restList = db.session.query(Rest).filter(Rest.name.in_(latestList)).all()    
    return sortRestLatest(restList)
    
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

def loc_query(lat,lng,radius,lim):
    return("SELECT * FROM (SELECT id, (3959 * acos(cos(radians({latitude})) * cos(radians(lat))\
    * cos(radians(lng) - radians({longitude})) + sin(radians({latitude}))\
    * sin(radians(lat)))) AS distance FROM rest) AS distance WHERE distance\
     < {radius} ORDER BY distance LIMIT {limit};".format(latitude=lat, longitude=lng, radius=radius,limit=lim)) 
 
def makeSlug(string,spaceChar='+',Maxlen=None):
            stringlst = string.split(" ")
            newStr =""
            for word in stringlst:
                newStr+=(word+spaceChar)        
            return newStr[:-1][:Maxlen]
          
if __name__ == "__main__":
    getLatest()