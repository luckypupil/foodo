from app import db
from datetime import date
import datetime
from sqlalchemy import func, Index
from datetime import timedelta
from sqlalchemy.orm import validates
from sqlalchemy.dialects import postgresql



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    zipcd = db.Column(db.Integer, nullable=True)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __init__(self, name, zipcd, first, last):
        self.email = name
        self.zipcd = zipcd
        self.first_name = first
        self.last_name = last

    def __repr__(self):
        return self.email


class Rest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    street = db.Column(db.Text)
    zipcd = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='rest', lazy='dynamic')
    lat = db.Column(db.Float(6))
    lng = db.Column(db.Float(6))
    tsv = db.Column(postgresql.TSVECTOR(), nullable=True, index=True)
    grade = db.Column(db.Text)
    #badges = db.Column(postgresql.ARRAY('Text'))

    def __init__(self, name, street, zipcd):
        self.name = name
        self.street = street
        self.zipcd = zipcd
     #   self.isvalid = True

    def __repr__(self):
        return '{}'.format(self.name)

    def jsond(self):
        instDict = {
            'id': self.id,
            'name': self.name,
            'street': self.street,
            'zipcd': self.zipcd,
            'lat': self.lat,
            'lng': self.lng,
        }
        return instDict

    def latestDt(self):
        latestDate = db.session.query(Comment.date).\
            filter(Rest.name == self.name).\
            filter(Rest.name == Comment.restnm).order_by(
                Comment.date.desc()).first()
        return (latestDate[0] if latestDate else None)
    
    def getVios(self):
         ### Violations for latestDt review####
        if self.latestDt():
             viosct = db.session.query(func.count(Comment.id)).\
                filter(Comment.restnm == self.name, Comment.date == self.latestDt()).first()
        
        try:
            return viosct[0]
        except:
            pass
             # Tuple list w/ # vios by dates w/in last year

    # def getVios(self):
    #     ### Average violations for last [365] days####
    #     vioCtList = db.session.query(func.count(Comment.id)).\
    #         filter(Comment.restnm == self.name,
    #                Comment.date > (date.today() - timedelta(days=765))).\
    #         group_by(Comment.date).all()
    #         # Tuple list w/ # vios by dates w/in last year

    #     # avg of vios from last year.  If none w/in year, '-1' returned
    #     avgVios = (None if len(vioCtList) == 0 else
    #                round(sum(float(date[0]) for date in vioCtList)
    #                      / float(len(vioCtList)), 1))
    #     if avgVios == None:
    #         self.isvalid = False
    #     return avgVios
        
        
    def getPts(self):
    	if self.latestDt():
	    	mytups = db.session.query(Comment.code).filter(Comment.date == self.latestDt(),
	    												   Comment.restnm == self.name).all()		
	        codelst = [i[0] for i in mytups]
	       
	       
	        def myfuct(code):
				return db.session.query(Badge.points).filter(Badge.code == code).first()[0]
	
	        points = sum((myfuct(i) for i in codelst))
        else:
        	points = None
        	
        return points


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    restnm = db.Column(db.String, db.ForeignKey('rest.name'))
    date = db.Column(db.Date, nullable=True)
    quote = db.Column(db.Text)
    code = db.Column(db.Integer, db.ForeignKey('badge.code'))


    def __init__(self, restnm, date, code, quote):
        self.restnm = restnm
        self.date = date
        self.code = code
        self.quote = quote

    def __repr__(self):
        return '{} : {}...'.format(self.date,
                                   str(self.quote.encode('utf-8'))[:40]
                                   )


class Badge(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True)
    badgenm = db.Column(db.String)
    points = db.Column(db.Float)
    category = db.Column(db.String)
    #rest = relationship("Rest", backref=backref('Rests', order_by=id))


    def __init__(self, code, badgenm):
        self.code = code
        self.badgenm = badgenm


    def __repr__(self):
        return '{}'.format(self.badgenm)
