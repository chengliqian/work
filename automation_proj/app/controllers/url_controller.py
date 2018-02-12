from . import url
from .. import db
from ..models import Url
from flask import jsonify, request


@url.route('/show', methods=['GET'])
def show():
	urls = []
	url = Url.query.all()
	print(url)
	if url:
		for u in url:
			print(u.to_json())
			urls.append(u.to_json())
	print(urls)
	return jsonify({'msg': urls})

@url.route('/add', methods=['POST'])
def add():
	pass

@url.route('/delete', methods=['POST'])
def delete():
	pass

@url.route('/update', methods=['POST'])
def update():
	req_data = request.json['query']
	print(req_data)
	url_id = req_data['id']
	u = Url.query.get(url_id)
	print(u)
	keys = req_data.keys()
	if 'name' in keys:
		u.desc = req_data['name']
	elif 'url' in keys:
		u.url = req_data['url']
	db.session.commit()

	return jsonify({'msg':'修改成功'})