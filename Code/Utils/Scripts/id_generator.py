class IdGenerator:
	def __init__(self):
		self.free_ids = set()
		self.highest_id = 0

	def get_id(self) -> int:
		if self.free_ids:
			return self.free_ids.pop()
        
		self.highest_id += 1
		return self.highest_id

	def release_id(self, element_id: int):
		self.free_ids.add(element_id)