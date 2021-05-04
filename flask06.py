# imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from database import db
from models import Event as Event
from models import User as User
from models import Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm
import bcrypt


app = Flask(__name__)  # create an app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_event_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'


# Bind SQLAlchemy db object to this Flask app
db.init_app(app)


# Setup models
with app.app_context():
    db.create_all()  # run under the app context


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
# @app.route('/')
@app.route('/index')
def index():
    # check if a user is saved in session
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")


@app.route('/events',methods=['GET', 'POST'])
def get_events():
    # # retrieve user from database
    # check if a user is saved in session
    if session.get('user'):
        other_events = db.session.query(Event).filter(Event.user_id != session['user_id']).all()
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()

        if request.method == "POST":
            if request.form.get("Sort_by_Name"):
                print("Sorting by Name...")
                other_events = db.session.query(Event).order_by(Event.event_title).filter(Event.user_id != session['user_id']).all()

            elif request.form.get("Sort_by_Date"):
                print("Sorting by Date...")
                other_events = db.session.query(Event).order_by(Event.event_date).filter(Event.user_id != session['user_id']).all()

        elif request.method == "GET":
            print("This shouldn't appear")

        return render_template('my_events.html', events=my_events, other_events=other_events, user=session['user'], userName=session['user_name'])
    else:
        return redirect(url_for('login'))


@app.route('/events/<event_id>/<event_type>')
def get_event(event_id, event_type):
    if session.get('user'):
        # create a comment form object
        form = CommentForm()

        if event_type == "user":
            # retrieve note from database
            my_event = db.session.query(Event).filter_by(id=event_id).one()
        elif event_type == "other":
            my_event = db.session.query(Event).filter(Event.user_id != session['user_id']).one()

        return render_template('event.html', event=my_event, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


@app.route('/events/new_event', methods=['GET', 'POST'])
def new_event():
    if session.get('user'):
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['eventText']
            # create data stamp
            event_date = formatDate(request.form['eventDate'])
            from datetime import date
            today = date.today()
            # format date
            today = today.strftime("%m-%d-%Y")
            new_record = Event(title, text, event_date, session['user_name'], session['user_id'], today)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            # GET request - show new note form
            return render_template('new_event.html', user=session['user'])
    else:
        # user is not in session redirect ot login
        return redirect(url_for('login'))


@app.route('/events/edit/<event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['eventText']
            event = db.session.query(Event).filter_by(id=event_id).one()
            # update note data
            event.title = title
            event.text = text
            # update note in DB
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            # GET request - show new note form to edit note
            # retrieve user from database
            my_event = db.session.query(Event).filter_by(id=event_id).one()

            return render_template('new_event.html', event=my_event, user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

    return render_template('new_event.html', event=my_event, user=a_user)


@app.route('/events.delete/<event_id>', methods=['POST'])
def delete_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        db.session.delete(my_event)
        db.session.commit()

        return redirect(url_for('get_events'))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        session['user_name'] = first_name + " " + last_name
        # show user dashboard view

        return redirect(url_for('get_events'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            session['user_name'] = the_user.first_name + " " + the_user.last_name
            # render view
            return redirect(url_for('get_events'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('login'))


@app.route('/events/<event_id>/comment', methods=['POST'])
def new_comment(event_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(event_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_event', event_id=event_id))

    else:
        return redirect(url_for('login'))

def formatDate(date): 
    return date[5:7] + '-' + date[8:10] + '-' + date[0:4]

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
