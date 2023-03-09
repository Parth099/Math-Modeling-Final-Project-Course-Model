import json as JSON

class JsonLoader:
	def __init__(self, path: str) -> None:
		self.data = None
		with open(path, 'r') as json_file:
			self.data = JSON.load(json_file)
