import requests
import json
import redis
import re
import urllib3
from .models import Url
from urllib.parse import urlunsplit, urlsplit, urlencode, parse_qs
urllib3.disable_warnings()

def set_query_parameter(url, param_name, param_value):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    print("----",type(query_params),query_params)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
# 易品:1, nexapi:2, nex后台:3, nex前台:4, omp:5
def get_session(category):
	try:
		s = _create_session(co=category)
		return s
	except Exception as e:
		raise e

def _create_session(co):
	s = requests.session()
	u = Url.query.filter_by(category=co).first()
	headers = {
		# "content-type": "application/json",
		"Accept": "application/json; text/plain, */*",
		"Accept-Encoding": "gzip, deflate, sdch"
	}

	if u.login_url and u.code_url:
		s.get(u.url + u.login_url, verify=False)
		s.get(u.url + u.code_url)
		verifyCode = _get_verifyCode(s, co, u)

	if co ==1:
		# header = {
		# 	"content-type": "application/json",
		# 	"Accept": "application/json; text/plain, */*",
		# 	"Accept-Encoding": "gzip, deflate, sdch"
		# }
		#headers.update({"content-type": "application/json"})
		cookie = {"Cookie":"vjuids=-1dc0c0889.157c25fef86.0.1476796f2f072; _ntes_nnid=8df4e14e04538dbb0d79a0a20b887a9e,1476434849681; _ntes_nuid=8df4e14e04538dbb0d79a0a20b887a9e; __gads=ID=e0d37b2259d6caa4:T=1482130018:S=ALNI_MYdpDN1MjTw_QGZXU_eEBR0DIYfeA; mail_psc_fingerprint=f2b2ae90f43bfe7e114f93a0edc5314c; vjlast=1476434850.1486619877.22; P_INFO=bjhaha123@163.com|1501209719|0|epayweb|00&99|bej&1501208579&epayweb#bej&null#10#0#0|&0|epayweb|bjhaha123@163.com; _ga=GA1.2.1968905868.1476775927; NTESbusiness-tomcatSI=807669C2B28287527522779C778D8782.hzbxs-yipin-qatest6.server.163.org-8011; al_tk=Zix2z8iiY5sECPCodxihe8wPe8V-wwvjFFqtYH4d_WNOmaWEhqQdvuFCxRfuZkr7b5U0QyCcUGFsjpDrzxsTzA"}

		# req = {
		# 	'name': u.login_name,
		# 	'password': u.login_password
		# 	# 'verifyCode': verifyCode
		# }
		# req.update({"authCode": verifyCode})
		# rep = s.post(u.url + u.real_login_url, data=req, headers=headers)
		# rep = s.post('http://10.165.124.27:8181/user/login', data=req, headers=headers)
		# print("Login para: ", req)
		# print("login URL: ", type(u.url + u.login_url), u.url + u.login_url)
		# print("Login OMP:", u.url + u.real_login_url, verifyCode, rep.text)
		# res = s.post('http://10.165.124.27:8181/user/userInfo').json()
		# token = res['user']['token']
	if co == 3:

		req = {
			'userName': u.login_name,
			'password': u.login_password
			# 'verifyCode': verifyCode
		}
		req.update({'verifyCode': verifyCode})
		headers.update({"content-type": "application/json"})
		s.post(u.url+u.real_login_url, data=json.dumps(req), headers=headers)
		return s
	if co == 5 or 6:
		req = {
			'name': u.login_name,
			'password': u.login_password
			# 'verifyCode': verifyCode
		}
		req.update({"authCode":verifyCode})
		rep = s.post(u.url+u.real_login_url, data=req, headers=headers)
		res = s.post(u.url + '/user/userInfo').json()
		token = res['user']['token']
		print("Token: ",token)
		#rep = s.post('http://10.165.124.27:8181/user/login', data=req, headers=headers)
		# print("Login para: ",req)
		# print("login URL: ",type(u.url+u.login_url),u.url+u.login_url)
		# print("Login OMP:",u.url+u.real_login_url,verifyCode,rep.text)

		return [s,token]

def _get_verifyCode(s, co, u):
	try:
		k = _get_verifyCode_key(s, co)
		rds = redis.Redis(host=u.redis_host, port=u.redis_port, password=u.redis_password)
		v = rds.get(k)
		verifyCode = v[-5:-1].decode()
		return verifyCode
	except Exception as e:
		raise e

def _get_verifyCode_key(s, co):
	try:
		# if co == 1:
		# 	k = 'session:ad.omp.b:{}'.format(s.cookies['loginUser'])
		# 	return k
		if co == 3:
			k = 'session:ad.nex.b:{}'.format(s.cookies['NEXSESSION'])
			return k
		if co == 4:
			k = 'session:ad.nex.f:{}'.format(s.cookies['NEXSESSION'])
			return k
		if co == 5 or 6:
			k = 'session:ad.omp.b:{}'.format(s.cookies['loginUser'])
			return k
	except Exception as e:
		raise e

if __name__ == '__main__':
	s = get_session(3)
	print(s)
