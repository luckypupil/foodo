#!/usr/bin/env
import requests
import json
from pprint import pprint 
from app.models import Rest
from app import db
import re

def geoCode(lmt=2000,):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    
    rest_list = Rest.query.filter_by(lat=None).limit(lmt).all()
    
    for rest in rest_list:
        street = rest.street
        street_list = street.split(" ")
        geo_str =""
        for word in street_list:
            geo_str+=(word+"+")
            
        address = geo_str[:-1]+"+Philadelphia,+PA"
        sensor = "false"
        key = "AIzaSyDZTlXL-J2h0DQO0CVDpXbtKOtn_TTCZTU"
         
        final_url = base_url+"address="+address+"&sensor="+sensor+"&key="+key
        r = requests.get(final_url)
        
        myobject =  r.json()
        
        if myobject['status'] == "OK":
            rest.lat = myobject["results"][0]["geometry"]["location"]["lat"]
            rest.lng = myobject["results"][0]["geometry"]["location"]["lng"]
            db.session.add(rest)
    
    db.session.commit()
    
if __name__ == "__main__":
    geoCode(10)
    