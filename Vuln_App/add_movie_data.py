from app import models, db

Movie=models.Movie

with open("final.txt", 'r') as in_file:
	for line in in_file:
		info = line.strip().split("|")
		movie = Movie(info[0], info[1], info[2], info[3], info[4])
		db.session.add(movie)
		db.session.commit()