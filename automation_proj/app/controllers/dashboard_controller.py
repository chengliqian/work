from . import dashboard
from ..models import User, NexApiCase
from flask import jsonify

@dashboard.route('/overview', methods=['GET', 'POST'])
def dashboard():
	user_count = User.count()
	case_count = NexApiCase.count()
	return jsonify({'msg': {'user_count': user_count, 'case_count': case_count}})