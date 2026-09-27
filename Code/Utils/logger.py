import os
import logging
from datetime import datetime


class ColumnAlignedFormatter(logging.Formatter):
	def format(self, record):
		f_name = record.filename[:25-len(str(record.lineno))-1]
		raw_src = f"{f_name}:{record.lineno}"
		record.file_and_line = raw_src[:25].ljust(25)
		
		return super().format(record)
	
class Logger():
	@staticmethod
	def initialize():
		logger = logging.getLogger()
		logger.setLevel(logging.DEBUG)
		
		logger.handlers.clear()

		log_format = '%(asctime)s | %(levelname)-8s | %(file_and_line)s > %(message)s'
		formatter = ColumnAlignedFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

		file_name = f'Logs/{datetime.now().strftime("%d.%m.%Y_%H-%M-%S.log")}'
		handlers = [
			logging.FileHandler(file_name, encoding="utf-8"),
			logging.StreamHandler()
		]

		for handler in handlers:
			handler.setFormatter(formatter)
			logger.addHandler(handler)

		# ==========================================
		#               Очистка логов
		# ==========================================
		folder = "Logs"
		if not os.path.exists(folder):
			os.makedirs(folder)

		try:
			files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.log')]
			files.sort(key=os.path.getmtime)
			if len(files) >= 25:
				count_to_delete = len(files) - 25 + 1
				for i in range(count_to_delete):
					os.remove(files[i])
		except Exception as e:
			print(f"Ошибка при очистке старых логов: {e}")
		