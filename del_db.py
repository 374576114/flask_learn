#! ./flask/bin/python

#del the db
from app.models import Post
from app import db

for post in Post.query.all():
    db.session.delete(post)
db.session.commit()
