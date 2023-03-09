import sys, os
sys.path.insert(0, os.getcwd()) # add this module to $path to allow python to find it later

import json as JSON

class JsonLoader:
	def __init__(self, path: str) -> None:
		self.data = None
		with open(path, 'r') as json_file:
			self.data = JSON.load(json_file)
