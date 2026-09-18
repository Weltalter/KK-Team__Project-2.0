from pathlib import Path


def export_data(library, file_name: str):
	json_data = library.model_dump_json(indent=4)

	with open(file_name, "w", encoding="utf-8") as f:
		f.write(json_data)

def import_data(library, file_name: str):
	path = Path(file_name)
	if not path.exists() or path.stat().st_size == 0:
		return None

	with open(file_name, "r", encoding="utf-8") as f:
		json_data = f.read()

	return library.model_validate_json(json_data)
