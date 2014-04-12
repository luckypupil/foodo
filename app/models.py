from app import db


class Rest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    street = db.Column(db.String(30))
    zipcd = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='rest', lazy='dynamic')
        
    def __init__(self,name,street,zipcd):
        self.name = name
        self.street = street
        self.zipcd = zipcd
        
    def __repr__(self):
        return '{}'.format(self.name)
    
    def getscore(self,codelist):
        pass
        
class Comment(db.Model):
    code_to_badge = {1:'rat badge',2:'roaches badge',3:'warm food'}
    
    id = db.Column(db.Integer, primary_key = True)
    restnm = db.Column(db.String, db.ForeignKey('rest.name'))
    date = db.Column(db.Date, nullable=True)
    quote = db.Column(db.String(325))
    code = db.Column(db.Integer)
    
    #rest = relationship("Rest", backref=backref('Rests', order_by=id)) 
    
    def __init__(self,restnm,date,code,quote):
        self.restnm = restnm
        self.date = date
        self.code = code
        self.quote = quote
    
    def getbadge(self,code):
        return code_to_badge[code]
    
        

    