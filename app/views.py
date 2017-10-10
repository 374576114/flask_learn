from flask import render_template, flash, redirect, \
        session, url_for, request,g
from flask_login import login_user, logout_user, \
        current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm

#add
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    u0 = { 'author':{'name':'MIC0'}, 'body':'Book0' }
    u1 = { 'author':{'name':'MIC1'}, 'body':'Book1' }
    u2 = { 'author':{'name':'MIC2'}, 'body':'Book2' }

    posts = [ u0, u1, u2 ]

    return render_template(
        'index.html',
        title = 'Home',
        user = user,
        posts = posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    #g.user.is_authenticated is atrribute 
    # not a function
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    flash('you will login .... ')
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        flash('Login requested for OpenId=' + form.openid.data +\
              ", remember me=" + str(form.remember_me.data))
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    flash('return to login html')
    return render_template(
        'login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS']
    )


@oid.after_login
def after_login(resp):
    if resp.email is None and resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None and nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        if user is None:
            return render_template('error.html',
                    error = 'user is none' +resp.email)
    remember_me =  False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
