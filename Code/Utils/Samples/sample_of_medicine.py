from dataclasses import dataclass
from datetime import date
from Code.Utils.Constants.sample_block import MedicineType, MedicineEffectSize


@dataclass
class MedicineSample:
    title: str = ''
    description: str = ''
    medicine_type: MedicineType = MedicineType.OTHER
    effect_size: MedicineEffectSize = MedicineEffectSize.MODERATE
    expiration_date: date = date.min
    is_stock: bool = True
    comment: str = ''
    instruction: str = ''
    hashtags: list = None

    def __post_init__(self):
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
    