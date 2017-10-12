from app import db
from hashlib import md5

class User(db.Model):
    '''
    if we change the table  elements
    we should './db_migrate.py' to upgrade our database
    '''
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

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
        return 'http://www.gravatar.com/avatar/' + \
                md5(self.email).hexdigest() + \
                '?d=mm&s=' + str(size)

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
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
