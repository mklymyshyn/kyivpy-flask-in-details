import minimongo as mm

from flask import Flask, flash, redirect, render_template
from flaskext.sqlalchemy import SQLAlchemy
from flask.ext.redis import init_redis
from flask.ext import wtf
from flask.ext.assets import Environment as AssetsEnvironment

from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore

from sqlalchemy.orm import scoped_session, sessionmaker

from assets import register_assets

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = 'samplesecretkey'
db = SQLAlchemy(app)
redis = init_redis(app)

assets = AssetsEnvironment(app)
#assets.debug = True
register_assets(assets)

#app.config['ASSETS_DEBUG'] = True
app.config['YUI_COMPRESSOR_PATH'] = 'contrib/yuicompressor-2.4.6.jar'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return u"%s" % self.username


class Profile(mm.Model):
    class Meta:
        database = "sampleproject"
        collection = "profiles"

        indices = (
            mm.Index('username'),
        )


class UserForm(wtf.Form):
    username = wtf.TextField(
        "Username", [wtf.Required()])
    email = wtf.TextField(
        "Email", [wtf.Required(), wtf.Email()])


# admin
admin_datastore = SQLAlchemyDatastore((User,), db.session)
admin_blueprint = admin.create_admin_blueprint(admin_datastore)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.route('/form', methods=['POST', 'GET'])
def form():
    form = UserForm()
    if form.validate_on_submit():
        flash("Success")
        return redirect("/form")
    return render_template("form.html",
            form=form)


@app.route('/')
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
