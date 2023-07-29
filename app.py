# app.py
from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    long_url = db.Column(db.String(2000), nullable=False)

    def __init__(self, short_code, long_url):
        self.short_code = short_code
        self.long_url = long_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    if not long_url:
        return 'Invalid URL', 400

    short_code = shortuuid.uuid()[:8]
    short_url = f"{request.host_url}{short_code}"

    url_mapping = ShortURL(short_code=short_code, long_url=long_url)
    db.session.add(url_mapping)
    db.session.commit()

    return f'Short URL: {short_url}'

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    url_mapping = ShortURL.query.filter_by(short_code=short_code).first()
    if url_mapping:
        return redirect(url_mapping.long_url)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
