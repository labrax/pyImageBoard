

"""Security mecanisms, like anti-flooding"""

import threading
from time import time
from table import Table

delay_time = 0

class AntiFlood():
	_ip_table = Table()
	
	def post(self, usr_id):
		self._ip_table.searchUpdate(usr_id, time())
	
	def delayToPost(self, usr_id):
		if self._ip_table.searchTable(usr_id) == -1:
			return 0
		elif ( time()-self._ip_table.getValue(self._ip_table.searchTable(usr_id)) ) > delay_time:
			return 0
		else:
			return delay_time - ( time()-self._ip_table.getValue(self._ip_table.searchTable(usr_id)) )
