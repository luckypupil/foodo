from app import db


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
    
    def name_slug(self):
        return self.name
        
class Comment(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    restnm = db.Column(db.String, db.ForeignKey('rest.name'))
    date = db.Column(db.Date, nullable=True)
    quote = db.Column(db.String)
    code = db.Column(db.Integer, db.ForeignKey('badge.code'))
    
    def __init__(self,restnm,date,code,quote):
        self.restnm = restnm
        self.date = date
        self.code = code
        self.quote = quote
        
    def __repr__(self):
        return '{} : {}...'.format(self.date,self.quote[:20])
    
#     def getbadge(self,code):
#         return code_to_badge[code]
    
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
        
        

    