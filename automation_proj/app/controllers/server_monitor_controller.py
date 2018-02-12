from . import mointor
from .. import db
from ..models.server_monitor import ServerMonitor
from flask_login import login_required, current_user
from flask import jsonify, current_app
from datetime import datetime
import json, psutil


@mointor.route('/all', methods=['GET', 'POST'])
def all():
	time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	mointor_info = ServerMonitor.query.filter(ServerMonitor.moniter_time<time)
	x_categories = []
	cpu = {'name': 'CPU', 'data':[]}
	memory = {'name': '内存', 'data': []}
	disks = {'name': '磁盘', 'data': []}
	series = []
	if mointor_info.count() > 0:
		for m in mointor_info:
			x_categories.append(m.moniter_time.strftime("%H:%M:%S"))
			cpu['data'].append(json.loads(m.cpu_info)['percent'])
			memory['data'].append(json.loads(m.memory_info)['percent'])
			disks['data'].append(json.loads(m.disks_info)['disk_usage_info']['percent'])

	series.append(memory)
	series.append(cpu)
	series.append(disks)
	# print(current_user.email)
	# test_worker.delay({"user":current_user.email})
	# print(current_user.email)
	# send_email.delay(current_user.email, 'test', '/mail/worker_email', countdown=20)

	return jsonify({'x_categories':x_categories, 'series':series})
