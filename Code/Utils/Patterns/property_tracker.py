import inspect


class PropertyTracker:
	def __init__(self, *args, **kwargs):
		super().__setattr__('is_changed', False)
		super().__init__(*args, **kwargs)

	def __setattr__(self, name, value):
		if name == 'is_changed':
			super().__setattr__(name, value)
			return

		is_internal = False
		frame = inspect.currentframe()
		try:
			while frame:
				func_name = frame.f_code.co_name
				if func_name in ('__init__', '__read_conf'):
					is_internal = True
					break
				frame = frame.f_back
		finally:
			del frame

		if not is_internal:
			current_value = getattr(self, name, None)
			if current_value != value:
				super().__setattr__('is_changed', True)

		super().__setattr__(name, value)
