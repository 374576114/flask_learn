from app import db, app
from hashlib import md5
import sys

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

#followers, table, not a model,
#so it is not a class, and query will be strange
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

class User(db.Model):
    '''
    if we change the table  elements
    we should './db_migrate.py' to upgrade our database
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    #nickname = db.Column(db.String(120), index = True, unique = True)
    nickname = db.Column(db.String(120), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) #python 2
        except NameError:
            return str(self.id) #python 3

    def __repr___(self):
        return '<User %r>' % (self.nickname)

    def avatar(self, size):
        index = 1
        return '/static/head/head ('+str(index) +').png'
        #return 'http://www.gravatar.com/avatar/' + \
        #        md5(self.email).hexdigest() + \
        #        '?d=mm&s=' + str(size)

    def follow(self, user):
        if not self.is_following(user):
            #print self.nickname+' follow '+user.nickname
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        #print self.nickname+' is_following '+user.nickname
        return self.followed.filter(
            followers.c.followed_id == user.id
            ).count() > 0

    def followed_posts(self):
        # join: Post.userid<-->followers.followed_id ==> a new table
        # filter follower_id == self.id 
        # order_by
        return Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
                ).filter( followers.c.follower_id == self.id).order_by(
                Post.timestamp.desc())



    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() == None:
                break
            version += 1
        return new_nickname

class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

if enable_search:
    whooshalchemy.whoosh_index(app, Post)
