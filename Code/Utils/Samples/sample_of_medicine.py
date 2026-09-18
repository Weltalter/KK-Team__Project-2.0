from datetime import date
from pydantic import BaseModel, model_validator
from Code.Utils.Constants.sample_block import MedicineType, MedicineEffectSize


class MedicineSample(BaseModel):
	title: str = ''
	description: str = ''
	medicine_type: MedicineType = MedicineType.OTHER
	effect_size: MedicineEffectSize = MedicineEffectSize.MODERATE
	expiration_date: date = date.min
	is_stock: bool = True
	comment: str = ''
	instruction: str = ''
	hashtags: list = None

	@model_validator(mode="after")
	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)
		
		return self

class MedicineLibrary(BaseModel):
	object_list: list[MedicineSample]
