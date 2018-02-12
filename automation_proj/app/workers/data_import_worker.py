from .. import celery, db, get_task_logger
from app.models import NexApiCase
from xlrd import open_workbook

logger = get_task_logger(__name__)

@celery.task(bind=True)
def import_case(self, filepath):
	logger.info('导入用例文件开始：{}'.format(filepath))
	bk = open_workbook(filepath, encoding_override="utf-8")
	try:
		sh = bk.sheets()[0]
	except:
		logger.info("no sheet in {} named sheet1".format(filepath))
		# raise "no sheet in %s named sheet1" % filepath
	else:
		nrows = sh.nrows
		ncols = sh.ncols
		for i in range(1, nrows):
			row_data = sh.row_values(i)
			name = row_data[0]
			desc = row_data[1]
			url = row_data[2]
			request_data = row_data[3]
			request_type = row_data[4]
			expectation = row_data[5]
			case = NexApiCase(name=name, desc=desc, url=url,
								request_data=request_data,
								request_type=request_type,
								expectation=expectation)
			db.session.add(case)

		logger.info("导入结束！")
