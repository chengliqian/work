from . import case
from .. import db, document_set
from ..models import NexApiCase, Url
from .forms.upload_form import UploadForm
from ..workers import import_case
from ..sessions import get_session,set_query_parameter
from flask import render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from xlrd import open_workbook
import os, sys,json,requests


@case.route('/show', methods=['GET'])
@login_required
def show_all():
    form = UploadForm()
    return render_template('cases.html', form=form)

@case.route('/show-case', methods=['GET'])
def show():
	case_id = request.args.get('id')
	case = NexApiCase.query.get(case_id).to_json()

	return jsonify({'msg': case})

@case.route('/get', methods=['POST'])
@login_required
def get():
	page= request.json['page']
	per_page = request.json['showData']
	co = request.json['category']
	pagination = NexApiCase.query.filter_by(category=co).paginate(page,
														per_page=per_page,
														error_out=True)
	cases = []
	for case in pagination.items:
		cases.append(case.to_json())

	total = NexApiCase.query.filter_by(category=co).count()

	return jsonify({'total': total, 'cases': cases})

@case.route('/update', methods=['POST'])
@login_required
def update():
	case_id = request.json['id']
	case = NexApiCase.query.get(case_id)
	case.name = request.json['name']
	case.desc = request.json['desc']
	case.url = request.json['url']
	case.request_type = request.json['request_type']
	case.request_data = request.json['request_data']
	case.expectation = request.json['expectation']
	# case.category = request.args.get('category')
	try:
		db.session.commit()
		# flash('用例更新成功')
		return jsonify({'msg': '用例更新成功'})
	except Exception as e:
		# flash('用例更新成功')
		return jsonify({'msg': '用例更新失败'})

@case.route('/delete', methods=['POST'])
@login_required
def delete():
	case_id = request.json['id']
	print(case_id)
	case = NexApiCase.query.get(case_id)
	try:
		db.session.delete(case)
		return jsonify({'msg': '用例删除成功'})
	except Exception as e:
		return jsonify({'msg': '用例删除失败'})

@case.route('/send', methods=['POST'])
@login_required
def send():
	id = request.json['id']
	case = NexApiCase.query.get(id)
	category = case.category
	data = case.request_data
	if data is None:
		data = {}
	u = Url.query.filter_by(category=category).first()
	YP_preurl = "http://qa.business.ka.163.com"
	header = {
		"content-type": "application/json",
		"Accept": "application/json; text/plain, */*",
		"Accept-Encoding": "gzip, deflate, sdch"
	}
	if category == 1:#易品
		# 易品cookie
		cookie = {"Cookie":"vjuids=-1dc0c0889.157c25fef86.0.1476796f2f072; "
						   "_ntes_nnid=8df4e14e04538dbb0d79a0a20b887a9e,1476434849681; "
						   "_ntes_nuid=8df4e14e04538dbb0d79a0a20b887a9e; "
						   "__gads=ID=e0d37b2259d6caa4:T=1482130018:S=ALNI_MYdpDN1MjTw_QGZXU_eEBR0DIYfeA; "
						   "mail_psc_fingerprint=f2b2ae90f43bfe7e114f93a0edc5314c; "
						   "vjlast=1476434850.1486619877.22; "
						   "P_INFO=bjhaha123@163.com|1501209719|0|epayweb|00&99|bej&1501208579&epayweb#bej&null#10#0#0|&0|epayweb|bjhaha123@163.com; _ga=GA1.2.1968905868.1476775927; "
						   "NTESbusiness-tomcatSI=807669C2B28287527522779C778D8782.hzbxs-yipin-qatest6.server.163.org-8011; "
						   "al_tk=Zix2z8iiY5sECPCodxihe8wPe8V-wwvjFFqtYH4d_WNOmaWEhqQdvuFCxRfuZkr7b5U0QyCcUGFsjpDrzxsTzA"}
		print('URL: ',YP_preurl+case.url)
		if case.request_type == 'post':
			res = requests.post(YP_preurl+case.url,data = data.encode('utf-8'),headers = header,cookies = cookie)
			print("执行结果：", res.text)
			return jsonify(
				{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': case.request_data, '结果: ': res.json()}})
		elif case.request_type == 'get':
			if case.expectation == "":#下载接口
				res = requests.get(YP_preurl+case.url, headers=header,cookies=cookie,stream = True)
				return jsonify(
					{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': data}})
			else:#非下载接口
				res = requests.get(YP_preurl+case.url, headers=header, cookies=cookie)
				print("执行结果：", res.text)
				return jsonify(
					{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': data, '结果: ': res.json()}})
	elif category == 5:
		session,token = get_session(category)
		#print("Session,Token: ",session,token)
		standard_url = set_query_parameter(u.url+case.url,"token",token)
		print("StandardURL: ",standard_url)
		# res = session.post(u.url + '/user/userInfo').json()
		# token = res['user']['token']
		if case.request_type == 'post':
			res = session.post(standard_url, data=data.encode('utf-8'), headers=header)
			print("执行结果：",res.text)

		elif case.request_type == 'get':
			res = session.get(standard_url, data=data.encode('utf-8'), headers=header)
			#res = session.get(u.url + case.url, headers=header)
			print("执行结果：", res.text)

		return jsonify({'msg':{'状态码: ': res.status_code, '地址: ': res.url, '参数: ':case.request_data, '结果: ': res.json()}})
	elif category == 6:
		session, token = get_session(category)
		standard_url = set_query_parameter(YP_preurl+case.url, "token", token)
		print("StandardURL: ", standard_url)
		if case.request_type == 'post':
			res = requests.post(standard_url, data=data.encode('utf-8'), headers=header)
			print("执行结果：", res.text)
			return jsonify(
				{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': case.request_data, '结果: ': res.json()}})

		elif case.request_type == 'get':
			if case.expectation == "":  # 下载接口
				res = requests.get(standard_url, headers=header,  stream=True)
				return jsonify(
					{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': data}})
			else:  # 非下载接口
				res = requests.get(standard_url, headers=header, )
				print("执行结果：", res.text)
				return jsonify(
					{'msg': {'状态码: ': res.status_code, '地址: ': res.url, '参数: ': data, '结果: ': res.json()}})

			# res = session.get(u.url + case.url, headers=header)
			print("执行结果：", res.text)



@case.route('/exc', methods=['POST'])
@login_required
def exc():
	case_ids = request.json['ids']
	total_num = len(case_ids)
	succeed_num = 0
	failed_num = 0
	failed_id = []
	dict = {1:{},5:{},6:{}}
	YP_preurl = "http://qa.business.ka.163.com"
	category_list = db.session.execute("select distinct category from nex_api_case where id in {};".format(tuple(case_ids)))
	for cat in category_list:
		catg = cat['category']
		if catg != 1:
			s= get_session(catg)
			dict[catg]['session'] = s[0]
			dict[catg]['token'] = s[1]
			u = Url.query.filter_by(category=catg).first()
			dict[catg]['pre_url'] =u.url
		elif catg ==1:
			dict[catg]['pre_url'] = YP_preurl
			dict[catg]['session'] = {}
			dict[catg]['token'] ={}


	cookie = {
		"Cookie": "vjuids=-1dc0c0889.157c25fef86.0.1476796f2f072; _ntes_nnid=8df4e14e04538dbb0d79a0a20b887a9e,1476434849681; _ntes_nuid=8df4e14e04538dbb0d79a0a20b887a9e; __gads=ID=e0d37b2259d6caa4:T=1482130018:S=ALNI_MYdpDN1MjTw_QGZXU_eEBR0DIYfeA; mail_psc_fingerprint=f2b2ae90f43bfe7e114f93a0edc5314c; vjlast=1476434850.1486619877.22; P_INFO=bjhaha123@163.com|1501209719|0|epayweb|00&99|bej&1501208579&epayweb#bej&null#10#0#0|&0|epayweb|bjhaha123@163.com; _ga=GA1.2.1968905868.1476775927; NTESbusiness-tomcatSI=807669C2B28287527522779C778D8782.hzbxs-yipin-qatest6.server.163.org-8011; al_tk=Zix2z8iiY5sECPCodxihe8wPe8V-wwvjFFqtYH4d_WNOmaWEhqQdvuFCxRfuZkr7b5U0QyCcUGFsjpDrzxsTzA"}

	header = {
		"content-type": "application/json",
		"Accept": "application/json; text/plain, */*",
		"Accept-Encoding": "gzip, deflate, sdch"
		}
	for cs_id in case_ids:
		case = NexApiCase.query.filter_by(id=cs_id).first()
		req_type = case.request_type
		category = case.category
		data = case.request_data
		if data is None:
			data = {}
		session = dict[category]['session']
		token = dict[category]['token']
		pre_url = dict[category]['pre_url']
		if category == 1:
			if req_type == 'post':
				# 此处添加请求逻辑
				res = requests.post(YP_preurl+case.url, data=data.encode('utf-8'), headers=header,cookies = cookie)
				print("执行结果：", type(res.text), res.text)
			elif req_type == 'get':
				res = requests.get(YP_preurl+case.url, data=data.encode('utf-8'),headers=header,cookies = cookie)
				print("执行结果：", res.text)
			if res.status_code == 200:
				succeed_num += 1
			else:
				failed_num += 1
				failed_id.append(cs_id)

		if category == 5:
		#session, token = get_session(5)
			standard_url = set_query_parameter(pre_url + case.url, "token", token)
			print("StandardURL: ", standard_url)
			if req_type == 'post':
				# 此处添加请求逻辑
				res = session.post(standard_url, data=data.encode('utf-8'), headers=header)
				print("执行结果：", type(res.text), res.text)
			elif req_type == 'get':
				res = session.get(standard_url, headers=header)
				print("执行结果：", res.text)

			if res.status_code == 200:
				res_text = json.loads(res.text)
				print("res_test:", res_text)
				if res_text['rs'] == 1 or res_text['rs'] == 2:
					# if int(res.text['rs'])==1 or int(res.text['rs'])==2:
					succeed_num += 1
				else:
					failed_num += 1
					failed_id.append(cs_id)
			else:
				failed_num += 1
				failed_id.append(cs_id)


		'''if category ==1:
			session = get_session(category)
			res = session.post(u.url + '/user/userInfo').json()
			token = res['user']['token']
			YP_preurl = "http://qa.business.ka.163.com"
			header = {
				"content-type": "application/json",
				"Accept": "application/json; text/plain, */*",
				"Accept-Encoding": "gzip, deflate, sdch"
			}

			req_data = json.loads(data)
			# req_data = eval(data)
			print("DICT:", type(req_data), req_data)
			request_data = json.dumps(req_data)
			if req_type == 'post':
				if case.url.endswith("token="):
					res = requests.post(YP_preurl + case.url + token, data=request_data.encode('utf-8'), headers=header,
										cookies=cookie)
				else:
					res = requests.post(YP_preurl + case.url, data=request_data.encode('utf-8'), headers=header,
										cookies=cookie)
				print("执行结果：", res.text)
			elif req_type == 'get':
				if case.url.endswith("token="):
					res = requests.get(YP_preurl + case.url + token, headers=header, cookies=cookie)
				else:
					res = requests.get(YP_preurl + case.url, headers=header, cookies=cookie)
				print("执行结果：", res.text)


			if res.status_code ==200:
				succeed_num += 1
			else:
				failed_num += 1
				failed_id.append(case_id)

		elif category == 5:
			session, token = get_session(category)
			standard_url = set_query_parameter(u.url + case.url, "token", token)
			print("StandardURL: ", standard_url)
			# res = session.post(u.url + '/user/userInfo').json()
			# token = res['user']['token']
			header = {
				# "Connection":"keep-alive",
				"content-type": "application/json",
				"Accept": "application/json; text/plain, */*",
				"Accept-Encoding": "gzip, deflate, sdch"
			}
			if req_type == 'post':
				# 此处添加请求逻辑

				res = session.post(standard_url, data=data.encode('utf-8'), headers=header)

				print("执行结果：", type(res.text),res.text)
			elif req_type == 'get':

				res = session.get(standard_url,headers=header)

				print("执行结果：",res.text)
			if res.status_code == 200 :
				res_text = json.loads(res.text)
				print("res_test:",res_text)
				if res_text['rs'] ==1 or res_text['rs'] == 2:
				#if int(res.text['rs'])==1 or int(res.text['rs'])==2:
					succeed_num += 1
				else:
					failed_num += 1
					failed_id.append(case_id)
			else:
				failed_num += 1
				failed_id.append(case_id)'''
		if category == 6:
		# header = {
		# 	# "Connection":"keep-alive",
		# 	"content-type": "application/json",
		# 	"Accept": "application/json; text/plain, */*",
		# 	"Accept-Encoding": "gzip, deflate, sdch"
		# }
			standard_url = set_query_parameter(YP_preurl + case.url, "token", token)
			print("StandardURL: ", standard_url)
			if req_type == 'post':
				res = requests.post(standard_url, data=data.encode('utf-8'), headers=header)
				print("执行结果：", res.text)
			elif req_type == 'get':
				res = requests.get(standard_url, data=data.encode('utf-8'), headers=header)
				# res = session.get(u.url + case.url, headers=header)
				#print("执行结果：", res.text)
			if res.status_code == 200:
				succeed_num += 1
			else:
				failed_num += 1
				failed_id.append(cs_id)

	message = {'msg':{'total_num':total_num, 'succeed_num':succeed_num, 'failed_num':failed_num, 'failed_id':failed_id}}
	flash("用例执行成功，详情请在测试报告查看。本次执行报告id: {}".format(1))
	return jsonify(message)

def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@case.route('/uploadajax', methods=['POST'])
def upldfile():
	if request.method == 'POST':
		files = request.files['file']
		if files and allowed_file(files.filename):
			if os.path.exists(sys.path[0]+'/app/static/uploads/'+files.filename):
				os.remove(sys.path[0]+'/app/static/uploads/'+files.filename)
			filepath = sys.path[0]+'/app/static/uploads/'+files.filename
			files.save(os.path.join(current_app.config['UPLOADED_DOCUMENT_DEST'], files.filename))
			file_size = os.path.getsize(current_app.config['UPLOADED_DOCUMENT_DEST']+files.filename)
			import_case.delay(filepath)
			return jsonify(name=files.filename, size=file_size)

@case.route('/upload', methods=['POST'])
@login_required
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		filename = form.upload.data.filename
		print(filename)
		if os.path.exists(sys.path[0]+'/app/static/uploads/'+filename):
			os.remove(sys.path[0]+'/app/static/uploads/'+filename)
		document_set.save(form.upload.data, name=filename)
		filepath = document_set.path(filename=filename)
		import_case.delay(filepath)
		flash("上传成功")
		return redirect(url_for('case.show_all'))
	flash("请先上传文件")
	return redirect(url_for('case.show_all'))