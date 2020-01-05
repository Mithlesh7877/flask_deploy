from Napp.forms import RegistrationForm,LoginForm,UpdateAccount
from flask import render_template
from flask import url_for,request
from flask import flash,redirect
from Napp import app,db,bcrypt
from Napp.models import User, Post
import secrets
import os
from flask_login import login_user,logout_user,current_user,login_required
#circular import problem

    

@app.route("/")
@app.route("/home")
def hello():
    posts = Post.query.all()
    #return "Hello"
    return render_template("home.html",posts=posts)
#what are decorator like route

@app.route("/about")
def abt():
    return render_template("about.html",title="About Title")

#@app.route("/login")
#def log():
#    return render_template("login.html",title="Login")

#@app.route("/register")
#def reg():
#    return render_template("register.html",title="Register")

@app.route("/register",methods=['GET','POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Account created now login",'success')#after creating database
        #flash(f"Account created for {form.username.data}!",'success')
        return redirect(url_for('log'))
    return render_template("register.html",title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def log():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello'))#ternary condition
        else:#if form.email.data=="mky@gmail.com" and form.password.data=="pass":
           #flash("Logged in","success")
           #return redirect(url_for("hello"))
            flash("Unsuccessful.","danger")          
    return render_template("login.html",title="Login",form=form)
#what is orm database

@app.route("/out")
def out():
    logout_user()
    return redirect(url_for("hello"))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.picture= picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template("account.html",title="Account",image_file=image_file,form=form)
'''
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('hello'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')
    '''
    