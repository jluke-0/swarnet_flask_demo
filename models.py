from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name =  db.Column(db.String, nullable=False)
    last_name =  db.Column(db.String, nullable=False)
    role_id= db.Column(db.Integer, nullable=False)
    username=db.Column(db.String,nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role_id': self.role_id,
            'username': self.username,
                      
        }
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
       return check_password_hash(self.password, password)
       
   # def __repr__(self):
       #return '<User {}>'.format(self.username)
       

     

class Topics(db.Model):
    topic_id=db.Column(db.Integer, primary_key=True)
    topicName=db.Column(db.String(80), unique=True)
    topicMessage=db.Column(db.String(120), nullable=False)
    topicCreator=db.Column(db.String, db.ForeignKey('user.username'))

    def toDict(self):
        return{
            'topic_id':self.topic_id,
            'topicName':self.topicName,
            'topicMessage':self.topicMessage,
            'topicCreator':self.topicCreator

        }

class Role(db.Model):
    userRole=db.Column(db.Integer, primary_key=True)
    roleName=db.Column(db.String, nullable=False)
    roleid=db.Column(db.Integer,db.ForeignKey('user.role_id'))

    def toDict(self):
        return{
            'userRole':self.userRole,
            'roleName':self.roleName,
            'roleid':self.roleid
        }

class Sub(db.Model):
  sub_id=db.Column(db.Integer, primary_key=True)
  sub_topic=db.Column(db.String, db.ForeignKey('topics.topicName'))
  sub_user=db.Column(db.String, db.ForeignKey('user.username'))
  randomcheck=db.Column(db.String, unique=True)
  

  def toDict(self):
    return{
      'sub_id':self.sub_id,
      'sub_topic':self.sub_topic,
      'sub_user':self.sub_user,
      'randomcheck':self.randomcheck
    }