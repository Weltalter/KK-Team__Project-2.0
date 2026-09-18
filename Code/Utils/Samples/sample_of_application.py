from Code.Utils.Constants.sample_block import BaseLibrary, BaseSample


class ApplicationSample(BaseSample):
	title: str = ''
	description: str = ''
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class ApplicationLibrary(BaseLibrary):
	object_list: list[ApplicationSample]
