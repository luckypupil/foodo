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
    FoodComments = {}
    OtherComments = {}
    #try:
    for commCodeTup in latComm:
         comm = commCodeTup[0]
         points = db.session.query(Badge.points).\
         		filter(Badge.code == commCodeTup[1]).first()[0]
         category = db.session.query(Badge.category).\
         		filter(Badge.code == commCodeTup[1]).first()[0]
         badge = db.session.query(Badge.badgenm).\
         		filter(Badge.code == commCodeTup[1]).first()[0]
         
         if category == 'Other': 
         	OtherComments.setdefault(badge,[]).append([comm,points])
         else:
         	FoodComments.setdefault(badge,[]).append([comm,points])     
    #except:
    	#BadgeNComments = None
    	
    return OtherComments,FoodComments
    #return [str(comm).decode('utf8').strip("(u'").strip("',)") for comm in latComm]


def getLatest(limit=20):
    ### returns list of Rest model objects ###
    latestTup = db.session.query(Comment.restnm).\
        group_by(Comment.restnm,Comment.date).order_by(Comment.date.desc()).limit(limit).all()
    latestList = [rest[0] for rest in latestTup]
    restList = db.session.query(Rest).filter(Rest.name.in_(latestList)).all()    
    return sorted(restList,key=methodcaller('latestDt'),reverse=True)


def get_grade(pts):
	### Converts points to equivalent inspection grade ###
	
	if pts == None: grade = 'N/A'
	elif pts <= 10: grade = 'A'
	elif pts <= 20: grade = 'B'
	elif pts <= 30: grade = 'C'
	elif pts <= 40: grade = 'D'
	elif pts > 40: grade = 'Fail'
	return grade
	
	
def loc_query(lat,lng,radius,lim):
    return("SELECT * FROM (SELECT id, (3959 * acos(cos(radians({latitude})) * cos(radians(lat))\
    * cos(radians(lng) - radians({longitude})) + sin(radians({latitude}))\
    * sin(radians(lat)))) AS distance FROM rest) AS distance WHERE distance\
     < {radius} ORDER BY distance LIMIT {limit};".format(latitude=lat, longitude=lng, radius=radius,limit=lim)) 
 

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