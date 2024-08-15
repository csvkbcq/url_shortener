from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Optional

class URLForm(FlaskForm):
    original_url = StringField('Original URL', validators=[DataRequired(), URL()])
    custom_id = StringField('Custom Short ID (optional)', validators=[Optional()])
    submit = SubmitField('Shorten URL')
