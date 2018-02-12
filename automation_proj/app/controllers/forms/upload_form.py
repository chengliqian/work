from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import document_set


class UploadForm(FlaskForm):
	upload = FileField('document', validators=[FileRequired(),
						FileAllowed(document_set, 'you can upload document only!')])
	submit = SubmitField('提交')
