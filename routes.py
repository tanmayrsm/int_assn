from flask import render_template ,url_for ,flash ,redirect ,request ,abort
from  flaskblog.models import User ,Check
from flaskblog.forms import RegistrationForm ,LoginForm ,UpdateAccount ,SearchForm,PostForm ,RequestResetForm ,ResetPasswordForm
from flaskblog import app, db ,bcrypt, mail	#__init__ se
from flask_login import login_user ,current_user ,logout_user ,login_required
import secrets ,os
from PIL import Image
from flask_mail import Message
import datetime

sear = []

def Remove(duplicate): 
	final_list = [] 
	for num in duplicate: 
		if num not in final_list: 
			final_list.append(num) 
	return final_list 

@app.route("/")
@app.route("/home")
def home():
	sear = []
	page = request.args.get('page' , 1 ,type = int)
	posts = Check.query.order_by(Check.date.desc()).paginate(page = page ,per_page = 2)

	l = len(Check.query.all())
	kero = []
	for i in range (0,l):
		g = Check.query.all()[i]
		f = datetime.datetime.now() - g.date
		l = divmod(f.total_seconds(), 60)
		if(l[0] > 1):
			kero.append(g)
	return render_template('home.html',posts = posts ,kero = kero)

@app.route("/about")
def about():
    return render_template('about.html',title = 'About')

@app.route("/charts")
def charts():
	l = len(Check.query.all())
	kero = []
	legend = "Histogram of time spent by vehicles"
	legendyo = "Vehicles who spent more than 4hrs in campus"
	val = []
	values = []
	labels = []
	for i in range (0,l):
		g = Check.query.all()[i]
		kero.append(g)
		f = datetime.datetime.now() - g.date
		p = divmod(f.total_seconds(), 60)
		
		values.append(p[0])

		labels.append(g.vehicle_no)
	return render_template('admin/examples/charts.html',legendyo = legendyo,val = val,legend  = legend,values  = values,labels = labels,length = len(kero))

@app.route("/search" ,methods = ['GET','POST'])
def search():

	form = SearchForm()
	l = len(Check.query.all())
	
	if form.validate_on_submit():

		s = form.search.data

		for i in range (0,l):
		    g = Check.query.all()[i]
		    if(s in g.vehicle_no or s in g.license):
		   		if g not in sear:
		   			sear.append(g)

	    		

		return redirect(url_for('search_items'))
	return render_template('search_now.html',title = 'Search', form = form)

@app.route("/search_items")
def search_items():
	k = len(sear)

	if k == 0:
		flash (f'Empty text !!', 'warning')
		return redirect(url_for('home'))
	
	return render_template('search.html',s = sear ,length = k)

@app.route("/noti")
def noti():
	l = len(Check.query.all())
	kero = []
	for i in range (0,l):
		g = Check.query.all()[i]
		f = datetime.datetime.now() - g.date
		l = divmod(f.total_seconds(), 60)
		if(l[0] > 1):
			kero.append(g)
	return render_template('noti.html',kero = kero,length = len(kero))

@app.route("/admin")
def admin():
	return render_template('admin/examples/dashboard.html')


@app.route("/register" ,methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data ,email = form.email.data,license = form.license.data, vehicle_no = form.vehicle_no.data)
		db.session.add(user)
		db.session.commit()
		flash (f'Vehicle with no :{form.vehicle_no.data} registered !', 'success')		
		#success category ....layout me dekh
		return redirect(url_for('home'))

	return render_template('register.html',title = 'Register', form = form)
# @app.route("/register")
# def register():
# 	form = RegistrationForm()
# 	return render_template('register.html',title = 'Register', form = form)
@app.route("/login",methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password ,form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page)if next_page else redirect(url_for('home'))
		else:
			flash('login unsuccessful chk email nd pawd!', 'danger')		
		#success category ....layout me dekh
	return render_template('login.html',title = 'Login', form = form)
# @app.route("/login")
# def login():
# 	form = LoginForm()
#     return render_template('login.html',title = 'Login', form = form)
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_post_picture(form_picture):
	random_hex = secrets.token_hex(8)	#8 bytes
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path ,'static/post_pic' ,picture_fn)
	form_picture.save(picture_path)
	
	return picture_fn


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)	#8 bytes
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path ,'static/profile_pic' ,picture_fn)
	output_size = (125 ,125)
	i  =Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods = ['GET','POST'])
def account():
	form = UpdateAccount()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		
		current_user.username  =form.username.data
		current_user.email = form.email.data
		current_user.vehicle  =form.vehicle.data
		current_user.license  =form.license.data
		
		db.session.commit()
		flash(f'Your Account has been updated' ,'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static' ,filename = 'profile_pic/' + current_user.image_file)
	return render_template('account.html',title = 'Account' ,image_file = image_file ,form = form)

@app.route("/post/new", methods = ['GET','POST'])
def new_post():
	form  = PostForm()
	if form.validate_on_submit():
		u = User.query.filter_by(vehicle_no = form.vehicle_no.data).first()
		if u == None :
			flash(f'Vehicle Not registered' ,'warning')
			return redirect(url_for('new_post'))
		
		if form.picture.data:
			picture_file = save_post_picture(form.picture.data)
		
			post = Check(vehicle_no = form.vehicle_no.data ,license = form.license.data ,
					image_file = picture_file)
			db.session.add(post)
			db.session.commit()
		image_file = url_for('static' ,filename = 'post_pic/' + picture_file)
		
		u = User.query.filter_by(vehicle_no = form.vehicle_no.data).first()
		print('u: ' ,u)
		if u == ' ':
			flash(f'Vehicle Not registered' ,'warning')
			return redirect(url_for('new_post'))
		return redirect(url_for('home'))
	else:
		image_file = url_for('static' ,filename = 'post_pic/default.jpg')
	return render_template('create_post.html',title = 'New Post', image_file = image_file ,
		form = form,legend = 'New post')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html' ,title = post.title ,post = post)

@app.route("/post/<int:post_id>/update",methods = ['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	form = PostForm()

	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_post_picture(form.picture.data)
			post.image_file = picture_file
		
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash ("Your post has been updated" ,'success')
		return redirect(url_for('post',post_id = post.id))

	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		form.picture.data = post.image_file
	image_file = url_for('static' ,filename = 'post_pic/' + post.image_file)
	return render_template('create_post.html',title = 'Update Post',
							form = form ,legend = 'Update post',image_file = image_file)		


@app.route("/post/<int:post_id>/delete",methods = ['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted','success')
	return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page' , 1 ,type = int)
	user = User.query.filter_by(username = username).first_or_404()
	posts = Post.query.filter_by(author  = user)\
			.order_by(Post.date.desc())\
			.paginate(page = page ,per_page = 2)
	return render_template('user_posts.html',posts = posts ,user = user)

