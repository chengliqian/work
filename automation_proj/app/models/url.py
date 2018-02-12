from app import db

class Url(db.Model):
	__tablename__ = 'url'

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(100))
	category = db.Column(db.Integer)
	desc = db.Column(db.String(100))
	login_url = db.Column(db.String(100))
	code_url = db.Column(db.String(100))
	real_login_url = db.Column(db.String(100))
	login_name = db.Column(db.String(100))
	login_password = db.Column(db.String(100))
	redis_host = db.Column(db.String(100))
	redis_port = db.Column(db.Integer)
	redis_password = db.Column(db.String(100))

	def __init__(
		self,
		url,
		category,
		desc,
		login_url,
		code_url,
		real_login_url,
		login_name,
		login_password,
		redis_host,
		redis_port,
		redis_password):

		self.url = url
		self.category = category
		self.desc = desc
		self.login_url = login_url
		self.code_url = code_url
		self.real_login_url = real_login_url
		self.login_name = login_name
		self.login_password = login_password
		self.redis_host = redis_host
		self.redis_port = redis_port
		self.redis_password = redis_password

	def to_json(self):
		url = {
			'id': self.id,
			'url': self.url,
			'category': self.category,
			'desc': self.desc,
			'login_url': self.login_url,
			'code_url': self.code_url,
			'real_login_url': self.real_login_url,
			'login_name': self.login_name,
			'login_password': self.login_password,
			'redis_host': self.redis_host,
			'redis_port': self.redis_port,
			'redis_password': self.redis_password
		}

		return url

	def __repr__(self):
		return '<Url {}>'.format(self.id)
