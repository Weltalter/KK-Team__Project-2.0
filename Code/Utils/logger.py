import logging
from datetime import datetime


class ColumnAlignedFormatter(logging.Formatter):
	def format(self, record):
		raw_src = f"{record.filename}:{record.lineno}"
		record.file_and_line = raw_src[:20].ljust(20)
		
		return super().format(record)
	
class Logger():
	@staticmethod
	def initialize():
		logger = logging.getLogger()
		logger.setLevel(logging.DEBUG)
		
		logger.handlers.clear()

		log_format = '%(asctime)s | %(levelname)-7s | %(file_and_line)s > %(message)s'
		formatter = ColumnAlignedFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

		file_name = datetime.now().strftime("%d.%m.%Y_%H-%M-%S.log")
		handlers = [
			logging.FileHandler(file_name, encoding="utf-8"),
			logging.StreamHandler()
		]

		for handler in handlers:
			handler.setFormatter(formatter)
			logger.addHandler(handler)