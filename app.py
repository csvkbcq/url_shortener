from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import URLForm
from models import db, URL
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

def generate_short_id(num_of_chars: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_of_chars))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        original_url = form.original_url.data
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = generate_short_id(6)
        short_url = URL(original_url=original_url, short_id=custom_id)
        db.session.add(short_url)
        db.session.commit()
        return render_template('result.html', short_url=request.host_url + custom_id)
    return render_template('index.html', form=form)

@app.route('/<short_id>')
def redirect_to_url(short_id):
    link = URL.query.filter_by(short_id=short_id).first_or_404()
    return redirect(link.original_url)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
