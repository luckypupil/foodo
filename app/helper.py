from app import db
from models import Comment, Rest, Badge
from sqlalchemy import func
import random
from datetime import date, timedelta
from operator import methodcaller
from pprint import pprint


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
    #Dict of badge and resulting comments from rest's most recent inspection#
    rest = Rest.query.get(restId)
    ltDt = rest.latestDt()
    latComm = db.session.query(Comment.quote,Comment.code).filter(Comment.restnm == rest.name,Comment.date == ltDt).all()
    BadgeNComments = {}
    #try:
    for commCodeTup in latComm:
         comm = commCodeTup[0]
         badge = db.session.query(Badge.badgenm).filter(Badge.code == commCodeTup[1]).first()[0]
         BadgeNComments.setdefault(badge,[]).append(comm)     
    #except:
    	#BadgeNComments = None
    	
    return BadgeNComments
    #return [str(comm).decode('utf8').strip("(u'").strip("',)") for comm in latComm]

def getVios(restId):
    ### Average violations for single rest####
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

def getLowest(limit=20):
    ### returns list of Rest model objects ###
    LowestTup = db.session.query(Comment.restnm).\
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

def get_grade(pts):
	### Converts points to equivalent inspection grade ###
	grade = 'n/a'
	if pts <= 7: grade = 'A'
	elif pts <= 12: grade = 'B'
	elif pts <= 20: grade = 'C'
	elif pts > 20: grade = 'Fail'
	
	return grade
	

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
 
def search_query(term):
	return("SELECT * FROM rest WHERE plainto_tsquery('{}') @@ tsv;".format(term))

def search2(lat,lng,radius,lim,term):
	return("SELECT * FROM (SELECT id, tsv, (3959 * acos(cos(radians({latitude})) * cos(radians(lat))\
    * cos(radians(lng) - radians({longitude})) + sin(radians({latitude}))\
    * sin(radians(lat)))) AS distance FROM rest) AS distance WHERE distance\
     < {radius} AND plainto_tsquery('{term}') @@ tsv ORDER BY distance LIMIT {limit};".format(latitude=lat, longitude=lng, radius=radius, term=term, limit=lim))
	
 
def makeSlug(string,spaceChar='+',Maxlen=None):
            stringlst = string.split(" ")
            newStr =""
            for word in stringlst:
                newStr+=(word+spaceChar)        
            return newStr[:-1][:Maxlen]
          
if __name__ == "__main__":
    getLatest()