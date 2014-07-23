
"""This class will handle cache of webpages"""

import os
from time import time
from table import Table

from threading import Lock

from definitions import cache_dir

cache_lock = Lock()

class Cache:
	_cache_table = Table()

	def __del__(self):
#		for i in range(0, self._cache_table.getLen()):
#			os.system("rm %s" % cache_dir + self._cache_table.getValue(i)[2])
		if self._cache_table.getLen() > 0:
			os.system("rm " + cache_dir + "cache_*")
		
		while self._cache_table.getLen() > 0:
			self._cache_table.pop()

	def isUpdated(self, thread):
		if self._cache_table.searchTable(thread) == -1:
			return False
		else:
			return True

	def setNotUpdated(self, thread):
		cache_lock.acquire()
		if self._cache_table.searchTable(thread) != -1:
			self._cache_table.pop(self._cache_table.searchTable(thread))
		cache_lock.release()

	def update(self, thread, content):
		content = str(content)
		new_elem = [str(thread), time(), len(content), "cache_"+str(thread)+".html"]
		
		return_point = self._cache_table.getValue(self._cache_table.searchTable(thread)) #in case it fails
		self._cache_table.searchUpdate(thread, [time(), len(content), "cache_"+str(thread)+".html"])
		
		try:
			fout = open(cache_dir + new_elem[3], "w")
			fout.write(content)
			fout.close()
		except IOError, e:
			if return_point == None:
				self._cache_table.pop(self._cache_table.searchTable(thread))
			else:
				self._cache_table.searchUpdate(thread, return_point)
			return "!!! Error: Cache %s cannot be written !!!" % str(thread)

	def getContent(self, thread):
		file_location = ""
		
		index = self._cache_table.searchTable(thread)
		if index == -1:
			return "!!! Error: Cache %s not found !!!" % str(thread)
		else:
			file_location = self._cache_table.getValue(index)[2]
			
		try:
			fin = open(cache_dir + file_location, "r")
		except IOError, e:
			# file could not be open, remove it from list of cached pages
			self.setNotUpdated(thread)
			return "!!! Error: Cache %s cannot be opened !!!" % str(thread)
		
		output = ""
		if fin:
			data_input = fin.read()
			while data_input:
				output += data_input
				data_input = fin.read()
			fin.close()

		return output
