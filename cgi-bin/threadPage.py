
"""This source contains the code for the thread page of the server."""

from web import form
from utils import upload, parsecontent, Output
from time import strftime

myform = form.Form(
	form.Textbox("User", style="width: 300px"),
	form.Textbox("E_mail", style="width: 300px"), 
	form.Textarea("Content", style="width: 300px; height: 150px;"),
	form.File("File", accept="image/jpg, image/gif, image/png, image/bmp"),
	)

class threadPage:
	_db = None
	_render = None
	_cache = None
	
	def __init__(self, db, render, cache):
		self._db = db
		self._render = render
		self._cache = cache
		
	def GET(self, thread):
		if self._cache.isUpdated(thread):
			return self._cache.getContent(thread)
		else:
			form = myform()
			content = self.list_posts(form, thread)
			self._cache.update(thread, content)
			return content

	def POST(self, thread, web):
		form = myform()
		if web.input().Content == "" and web.input(File={}).File.filename == "":
			return Output().pageReturnErrorSubFolder("To be able to post you need to add text or image!")
		else:
			self._cache.setNotUpdated(0)
			self._cache.setNotUpdated(thread)
			return upload().get(web, self._db, thread)


	def list_posts(self, form, thread):
		output = ""
		try:
			thread = int(thread)
		except ValueError, e:
			return Output().pageReturnErrorSubFolderRefreshBack("Invalid or deleted thread!")
			
		posts = self._db.list_posts(thread)
		
		if len(posts) == 0:
			return Output().pageReturnErrorSubFolderRefreshBack("Invalid or deleted thread!")
		
		return self._render.thread_part_template(posts, form, parsecontent, strftime("%a, %d %b %Y %H:%M:%S %Z"))
