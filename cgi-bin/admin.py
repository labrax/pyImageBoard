

"""This page implements admin tools for the server"""

from threading import Lock
from table import Table

i_lock = Lock()

class Statistics:
	_table = None
	
	def __init__(self):
		self._table = Table()
	
	def increment(self, index_content):
		i_lock.acquire()
		initial_value = self._table.getValue(self._table.searchTable(index_content))
		if initial_value == None:
			initial_value = 0
		self._table.searchUpdate(index_content, initial_value+1)
		i_lock.release()

	def printAll(self):
		for i in range(0, self._table.getLen()):
			print self._table.getIndex(i), self._table.getValue(i)
