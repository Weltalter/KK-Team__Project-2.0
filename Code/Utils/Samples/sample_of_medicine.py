from datetime import date
from Code.Utils.Constants.sample_block import BaseLibrary, BaseSample, MedicineType, MedicineEffectSize


class MedicineSample(BaseSample):
	title: str = ''
	description: str = ''
	medicine_type: MedicineType = MedicineType.OTHER
	effect_size: MedicineEffectSize = MedicineEffectSize.MODERATE
	expiration_date: date = date.min
	is_stock: bool = True
	comment: str = ''
	instruction: str = ''
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class MedicineLibrary(BaseLibrary):
	object_list: list[MedicineSample]
