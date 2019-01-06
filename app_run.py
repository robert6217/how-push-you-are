import requests
from flask import *
from predict import *
from Model.FBdb import *
from functools import wraps
from datetime import timedelta
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'ee11cf35a1ae0bdd35f06ef151fb004d'
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.session_protection       = "strong"
login_manager.login_view               = "login"
login_manager.login_message            = "Please LOG IN"
login_manager.login_message_category   = "info"
login_manager.remember_cookie_duration = timedelta(days=1)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    
class User(UserMixin):
    pass


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_fun = func(*args, **kwargs)
        return json.dumps(get_fun)

    return wrapper


def query_FBuser(FBuserID):
    FBuser = UserAccounts.query.filter_by(FBuserID=FBuserID).first()
    if FBuser:
        return True
    return False

@login_manager.user_loader
def user_loader(username):
    if query_FBuser(username):
        user = User()
        user.id = username
        return user
    return None

@app.route('/')
@app.route('/index')
@login_required
def index():
    user_id = session.get('user_id')
    user = UserAccounts.query.filter_by(FBuserID=user_id).first()

    if user:
        if user.UserName == None:
            data = requests.get(
                "https://graph.facebook.com/me?fields=id,name,picture.type(large)&access_token=" + user.FBAccessToken)
            if data.status_code == 200:
                FBuserID  = data.json()['id']
                FBuser    = data.json()['name']
                FBpicture = data.json()['picture']['data']['url']
                user.FBuserID = FBuserID
                user.UserName = FBuser
                user.UserPic  = FBpicture
                db.session.add(user)
                db.session.commit()
                predictData = howPush(FBpicture, FBuserID)
                if 99 > predictData['push'] > 9:
                    number_color = 'yellow-text text-accent-3'
                elif predictData['push'] < 10:
                    number_color = 'light-green-text text-accent-3'
                elif predictData['push'] == '爆':
                    number_color = 'deep-orange-text'
        else:
            FBuser    = user.UserName
            FBpicture = user.UserPic
            predictData = howPush(FBpicture, user_id)
            if 99 > predictData['push'] > 9:
                number_color = 'yellow-text text-accent-3'
            elif predictData['push'] < 10:
                number_color = 'light-green-text text-accent-3'
            elif predictData['push'] == '爆':
                number_color = 'deep-orange-text'
    else:
        FBuser    = ""
        FBpicture = ""
    return render_template("index.html", **locals())


@app.route('/about')
def about():
    return render_template("about.html", **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')
    print('/login, user_id: %s, login' %user_id)
    if request.method == 'GET':
        return render_template("login.html")

    if query_FBuser(user_id):
        return redirect(url_for('index'))

@app.route('/API_FB_login', methods=['POST'])
@to_json
def API_FB_login():
    userID = request.json['userID']
    print('/API_FB_login, userID: %s, login' %userID)
    accessToken = request.json['accessToken']
    FBuserID_Exist = UserAccounts.query.filter_by(FBuserID=userID).first()
    if FBuserID_Exist == None:
        newAccount = UserAccounts(UserName=None, UserPic=None, FBuserID=userID, FBAccessToken=accessToken)
        db.session.add(newAccount)
        user = User()
        user.id = userID
        login_user(user, remember=True)
    else:
        FBuserID_Exist.FBAccessToken = accessToken
        db.session.add(FBuserID_Exist)
        user = User()
        user.id      = FBuserID_Exist.FBuserID
        user.picture = FBuserID_Exist.UserPic
        login_user(user, remember=True)
    db.session.commit()
    return "11"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)