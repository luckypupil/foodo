#!/usr/bin/env python
from app import db
from app.models import User, Rest, Comment, Badge
from pprint import pprint as pp
from app.helper import get_grade

def main():


	def UpdateAllRestGrades():
		rests = db.session.query(Rest).all()
		for rest in rests:
			rest.grade = get_grade(rest.getPts())
			db.session.add(rest)
			db.session.commit()

			# restpts = [(rest,rest.getPts(),get_grade(rest.getPts())) for rest in rests]
		

	return UpdateAllRestGrades()	

if __name__ == "__main__":
	main()



