class DataScripts():
	def items_to_dict(items: list[tuple[str, str]], type: type) -> dict:
		return {k: type(v) for k, v in items}
