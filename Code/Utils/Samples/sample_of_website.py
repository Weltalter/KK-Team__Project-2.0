from Code.Utils.Constants.sample_block import BaseLibrary, BaseSample


class WebsiteSample(BaseSample):
	title: str = ''
	url: str = ''
	description: str = ''
	vpn: bool = False
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class WebsiteLibrary(BaseLibrary):
	object_list: list[WebsiteSample]
