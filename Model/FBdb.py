from flask import Flask
from datetime import datetime
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://cnovdkswwvqffm:a619a3d1912ab71a02ad172c86bf4d81939e4145f5db9d5b91abf6413779644f@ec2-107-20-237-78.compute-1.amazonaws.com:5432/d43m73r4rvn111'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class UserAccounts(db.Model):
    __tablename__ = 'UserAccounts'

    Id            = db.Column(db.Integer, primary_key=True)
    UserName      = db.Column(db.String(10))
    UserPic       = db.Column(db.Text)
    FBuserID      = db.Column(db.String(30))
    FBAccessToken = db.Column(db.String(256))
    CreateDate    = db.Column(db.DateTime)
    ModifiedDate  = db.Column(db.DateTime)

    def __init__(self
                 , UserName
                 , UserPic
                 , FBuserID
                 , FBAccessToken
                 , CreateDate=datetime.now()
                 , ModifiedDate=datetime.now()
                 ):
        self.UserName      = UserName
        self.UserPic       = UserPic
        self.FBuserID      = FBuserID
        self.FBAccessToken = FBAccessToken
        self.CreateDate    = CreateDate
        self.ModifiedDate  = ModifiedDate

    def update(self):
        db.session.commit()

if __name__ == '__main__':
    manager.run()
