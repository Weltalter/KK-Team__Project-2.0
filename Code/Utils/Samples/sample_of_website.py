from pydantic import BaseModel, model_validator


class WebsiteSample(BaseModel):
	title: str = ''
	url: str = ''
	description: str = ''
	vpn: bool = False
	hashtags: list = None

	@model_validator(mode="after")
	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)
		
		return self

class WebsiteLibrary(BaseModel):
	object_list: list[WebsiteSample]
