from app import db
from models import Comment, Rest
import random



def make_badges(rest_id):
    rest = Rest.query.get(rest_id)
    badges = []
    for comment in rest.comments.all():
        if comment.code not in badges:
            badges.append(comment.code)
    return badges

def create_badge_list():
    options = ['rats','roaches','High Food Temp','Spoiled Milk']
    badge_list = []
    for i in xrange(56):
        badge = random.choice(options)
        badge_list.append(badge)
    return badge_list    
                
     
# code_to_badge = [    