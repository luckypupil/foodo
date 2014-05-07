from app import db
from models import Comment, Rest, Badge
import random



def make_badges(restId):
    ### Return unique badge list for restaurant ###
    rest = Rest.query.get(restId)
    badges = []
    for comment in rest.comments.all():
        badge = Badge.query.filter_by(code=comment.code).first()
        if badge and badge.badgenm not in badges:
            badges.append(badge.badgenm)
    return badges

def getPoints(restId):
    rest = Rest.query.get(restId)
    latestDate = Comment.query.filter_by(restnm=rest.name).order_by(Comment.date.desc()).limit(2).date
    latestComments = Comment.query.filter_by(restnm=rest.name).filter_by(date=latestDate).all()
    return {'date':latestDate,'comments':latestComments,'points':len(latestComments)} 
    
    
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
    loc_query()