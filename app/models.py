from app import db
from datetime import date


class Rest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    street = db.Column(db.Text)
    zipcd = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='rest', lazy='dynamic')
    lat = db.Column(db.Float(6))
    lng = db.Column(db.Float(6))
        
    def __init__(self,name,street,zipcd):
        self.name = name
        self.street = street
        self.zipcd = zipcd
        
    def __repr__(self):
        return '{}'.format(self.name)
    
    def jsond(self):
        instDict = {
            'id':self.id,
            'name':self.name,
            'street':self.street,
            'zipcd':self.zipcd,
            'lat': self.lat,
            'lng':self.lng,
            }
        return instDict
    
    def getLatest(self):
        latestDate = db.session.query(Comment.date).filter(Rest.name == self.name).\
            filter(Rest.name == Comment.restnm).order_by(Comment.date.desc()).first()[0]
        latestDate = latestDate.date()
        return latestDate
        
class Comment(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    restnm = db.Column(db.String, db.ForeignKey('rest.name'))
    date = db.Column(db.Date, nullable=True)
    quote = db.Column(db.Text)
    code = db.Column(db.Integer, db.ForeignKey('badge.code'))
    
    def __init__(self,restnm,date,code,quote):
        self.restnm = restnm
        self.date = date
        self.code = code
        self.quote = quote
        
    def __repr__(self):
        return '{} : {}...'.format(self.date,str(self.quote.encode('utf-8'))[:40])
    
    
class Badge(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Integer, unique = True )
    badgenm = db.Column(db.String)
    #rest = relationship("Rest", backref=backref('Rests', order_by=id)) 
    
    def __init__(self,code,badgenm):
        self.code = code
        self.badgenm = badgenm
        
    def __repr__(self):
        return '{}'.format(self.badgenm)
        
        

    