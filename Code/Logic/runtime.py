from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.libraries import *

class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		pass

	def run(self):
		test1 = ApplicationSample(title='TITLE_test1', description='DESCRIPTION_test1', hashtags=['1', '2', '3'])
		test2 = ApplicationSample(title='TITLE_test2', description='DESCRIPTION_test2', hashtags=['1', '2', '3'])
		al1 = ApplicationLibrary()
		al1.add(test1)
		al2 = ApplicationLibrary()
		al2.add(test2)
		al1.export_data('TEST')
		lib = al1.import_data('TEST')
		lib.remove(test1.sample_id)
		lib.export_data('TEST2')

