from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.libraries import *
from Code.Logic.data_file_system import export_data, import_data

class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		pass

	def run(self):
		test = ApplicationSample(title='TITLE_test', description='DESCRIPTION_test', hashtags=['1', '2', '3'])
		al = ApplicationLibrary()
		al.object_list.append(test)
		export_data(al, 'TEST')

