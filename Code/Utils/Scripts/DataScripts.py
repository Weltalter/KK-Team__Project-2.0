class DataScripts():
	def itemsToDict(items: list[tuple[str, str]], type: type, coordinate_flag=False) -> dict:
		if coordinate_flag: return {k: type(int(v) *.8) for k, v in items}
		else: return {k: type(v) for k, v in items}
