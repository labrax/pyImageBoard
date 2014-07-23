
"""This source contains the code for the root page of the server."""

from web import form
from utils import upload, parsecontent, Output
from time import strftime

myform = form.Form(
	form.Textbox("User", style="width: 300px"),
	form.Textbox("E_mail", style="width: 300px"), 
	form.Textarea("Content", style="width: 300px; height: 150px;"),
	form.File("File", form.notnull, accept="image/jpg, image/gif, image/png, image/bmp",),
	)


class rootPage:
	_db = None
	_render = None
	_cache = None
	
	def __init__(self, db, render, cache):
		self._db = db
		self._render = render
		self._cache = cache
		
	def GET(self):
		if self._cache.isUpdated(0):
			return self._cache.getContent(0)
		else:
			form = myform()
			content = self._render.thread_outside_template(form, self.list_threads(), parsecontent, self._db, strftime("%a, %d %b %Y %H:%M:%S %Z"))
			self._cache.update(0, content)
			return content

	def POST(self, web):
		form = myform()
		if not form.validates():
			return Output().pageReturnError("To be able to post you need to add image!")
		else:
			self._cache.setNotUpdated(0)
			return upload().get(web, self._db, 0)

	def list_threads(self):
		return self._db.list_threads()

