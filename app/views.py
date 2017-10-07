from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'name':'CraboYang'} #fake user
	u0 = { 'author':{'name':'MIC0', 'body':'Book0'} }
	u1 = { 'author':{'name':'MIC1', 'body':'Book1'} }
	u2 = { 'author':{'name':'MIC2', 'body':'Book2'} }

	posts = [ u0, u1, u2 ]

	return render_template(
			'index.html',
			title = 'Home',
			user = user,
			posts = posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenId=' + form.openid.data +\
				", remember me=" + str(form.remember_me.data))
		return redirect('/index')
	return render_template(
			'login.html',
			title = 'Sign In',
			form = form,
			providers = app.config['OPENID_PROVIDERS']
			)
