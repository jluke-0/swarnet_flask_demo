import json
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError

from models import db, User, Topics,Role,Sub

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

''' Set up JWT here '''
def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

''' End JWT Setup '''

#######JINJA TEMPLATES FOR DEMO#######
@app.route('/')
def make_users():
  db.create_all(app=app)
  print(app.config['SQLALCHEMY_DATABASE_URI'])
  print('database initialized!')
  bob = User(first_name="Bob", last_name="Smith",role_id=1,username="bobby")
  bob.set_password("bobp")
  db.session.add(bob)
  rob=User(first_name="Rob", last_name="Franklin",role_id=2,username="rob@email.com")
  rob.set_password("robp")
  db.session.add(rob)
  rose=User(first_name="Rose", last_name="Flower",role_id=2,username="roseF")
  rose.set_password("rosep")
  db.session.add(rose)
  #subS=Sub(sub_topic="This topic",sub_user=bob.username)
  #db.session.add(subS)
  #topicTest=Topics(topicName="Testing",topicMessage="Testing this message")
  #db.session.add(topicTest)
  db.session.commit()
  #print("user created: "+bob.username)
  #print(bob.role_id)
  return render_template('index.html')


@app.route('/login')
def loginpage(): #perhaps remove
  return render_template('login.html')


@app.route('/users')
def index():
  users=User.query.all()
  return render_template('users.html',users=users)

@app.route('/users/<id>/home')
def user_page(id):
  user=User.query.filter_by(id=id).first_or_404()
  topic=Topics.query.all()
  return render_template('home.html',user=user,topic=topic)

@app.route('/topics')
def all_topics():
  topic=Topics.query.all()
  return render_template('topics.html',topic=topic)

@app.route('/subscriptions')
def all_subs():
  sub=Sub.query.all()
  return render_template('subscriptions.html',sub=sub)


@app.route('/created/<id>', methods=['POST'])
def insert_action(id):
  data=request.form['topic'] #gets topic name
  data2=request.form['message'] #gets message
  user=User.query.filter_by(id=id).first_or_404()
  #print(user.id)
  username=user.username
  newTopic=Topics(topicName=data,topicMessage=data2,topicCreator=username)
  try:
    db.session.add(newTopic)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()
    return render_template('notcreated.html')
  return render_template('created.html') 

@app.route('/sub/<topicName>/<id>',methods=['POST'])
def sub(id,topicName):
  user=User.query.filter_by(id=id).first_or_404()
  username=user.username
  check=username+topicName #unique string generated to not duplicate users
  #print(check)
  #print(username)
  #print(topicName)
  newSub=Sub(sub_topic=topicName,sub_user=username,randomcheck=check)
  if request.form['subscribe']=='subscribe':
    try:
      db.session.add(newSub)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
      return render_template('alreadysubbed.html')     
    return render_template('subbed.html')

@app.route('/unsub/<topicName>/<id>',methods=['POST'])
def unsub(id,topicName):
  user=User.query.filter_by(id=id).first_or_404()
  username=user.username
  check=username+topicName 
  if request.form['unsubscribe']=='unsubscribe':
    unsub=Sub.query.filter_by(randomcheck=check).first_or_404()
    db.session.delete(unsub)
    db.session.commit()
    return render_template('unsub.html')

#######REST API / HEADLESS WITH NO UI#######
@app.route('/api/topics')
def api_topics():
  topic=Topics.query.all()
  topic=[topic.toDict() for topic in topic]
  return json.dumps(topic)

@app.route('/api/users')
def api_users():
  users=User.query.all()
  users=[users.toDict() for users in users]
  return json.dumps(users)

@app.route('/api/subscriptions')
def api_subs():
  sub=Sub.query.all()
  sub=[sub.toDict()for sub in sub]
  return json.dumps(sub)

@app.route('/api')
def api():
  topic=Topics.query.all()
  topic=[topic.toDict() for topic in topic] 
  users=User.query.all()
  users=[users.toDict() for users in users]
  sub=Sub.query.all()
  sub=[sub.toDict()for sub in sub]
  all = [sub, topic,users]
  return json.dumps(all)









app.run(host='0.0.0.0', port=8080)