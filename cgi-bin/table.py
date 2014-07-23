
"""This file will define the table used by multiple sources on memory"""

import threading

class Table:
	_index_cache = None
	_table = None
	_content_column = None
	
	_lock_table = None
	
	def __init__(self, content_column=1):
		self._index_cache = 0
		self._table = []
		self._content_column = content_column
		self._lock_table = threading.Lock()
	
	def searchUpdate(self, index_content, content, create=True, content_column=0):
		self._lock_table.acquire()
		if self.searchTable(index_content) == -1:
			if create == True:
				self._table.append([str(index_content), content])
			else:
				self._lock_table.release()
				return False
		else:
			if content_column == 0:
				self._table[self.searchTable(index_content)][self._content_column] = content
			else:
				self._table[self.searchTable(index_content)][content_column] = content
		self._table.sort()
		self._lock_table.release()
		return True
	
	def getLen(self):
		return len(self._table)
	
	def pop(self, index=-1):
		self._lock_table.acquire()
		r=self._table.pop(index)
		self._lock_table.release()
		
	def getTable(self):
		return self._table
		
	def setTable(self, table):
		self._lock_table.acquire()
		self._table = table
		self._lock_table.release()
	
	def update(self, index, content, content_column=0):
		self._lock_table.acquire()
		if content_column == 0:
			self._table[index][self._content_column] = content
		else:
			self._table[index][content_column] = content
		self._lock_table.release()
	
	def getValue(self, index, content_column=0):
		if index == -1:
			return None
		if content_column == 0:
			return self._table[index][self._content_column]
		else:
			return self._table[index][self.content_column]
	
	def getIndex(self, index):
		if index == -1:
			return None
		else:
			return self._table[index][0]
	
	def append(self, index_content, content):
		self._lock_table.acquire()
		self._table.append([str(index_content), content])
		self._table.sort()
		self._lock_table.release()
	
	def searchTable(self, index_content, search_cache=True):
		#print "start table"
		#for row in self._table:
		#	print row
		#print "finish table"

		if len(self._table) == 0:
			return -1

		searching_for = str(index_content) #can make comparison between strings
		
		if self._index_cache < len(self._table) and self._table[self._index_cache][0] == searching_for:
			return self._index_cache

		inferior_limit = 0
		superior_limit = len(self._table)
		
		search_index = int(superior_limit/2)
		
		previous_index = search_index
		
		while searching_for != self._table[search_index][0]:
			if searching_for < self._table[search_index][0]:
				superior_limit = search_index
				search_index = int((superior_limit-inferior_limit)/2)
				if search_index > superior_limit:
					search_index = superior_limit
			else:
				inferior_limit = search_index
				search_index = int((superior_limit-inferior_limit)/2)
				if search_index < inferior_limit:
					search_index = inferior_limit
			if(search_index == previous_index):
				break
			previous_index = search_index
		
		if self._table[search_index][0] == searching_for:
			if search_cache == True:
				self._index_cache = search_index
			else:
				self._index_cache = 0
			return search_index
		else:
			return -1
