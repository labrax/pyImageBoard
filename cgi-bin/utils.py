
"""This source contains the code for the treatment of images from the server."""

import os
import Image
from math import ceil
import hashlib

from definitions import temp_dir, img_dir

folder_on_fail = "../static/"
img_on_fail = 'something_ww.jpg' #image that return on fail to get one

dir_up = temp_dir #place for the temporary uploaded files

cut_post_lines = 16

class upload:
	def get(self, web, db, thread):
		x = web.input(File={})
		
		e_mail = web.input().E_mail
		usr = "Anonymous"
		if (e_mail == "sage"):
			usr = "Heaven"
			e_mail = ""
		elif(len(web.input().User) > 0):
			usr = web.input().User
		
		content = self.pre_parsecontent(web.input().Content)
		new_img = ""
		img_name = ""
		sha1 = ""
		img_id = ""
		post_id = db.id()
		usr_ip = web.ctx.ip
		
		img_thumb_X = 0
		img_thumb_Y = 0
		img_size = 0
		img_dim = ""
		
		if(x.File.filename != ""):
			ftemp = x.File.file.read()
			
			sha1 = str(hashlib.sha1(ftemp).hexdigest())
			if self.exists_in_bd(db, sha1) is True:
				return Output().pageReturn("Image already in db!")
				
			fout = open(dir_up + x.File.filename.replace(" ", "_"), "w")
			fout.write(ftemp)
			fout.close()
			if(self.check_is_image(dir_up + x.File.filename) is False): #image already existed in bd or is invalid
				if thread == 0:
					return Output().pageReturn("Not an image!")
				else:
					return Output().pageReturnErrorSubFolder("Not an image!")
			else:
				img_id = db.id_img()
				
				new_img = str(img_id) + '.' + x.File.filename.split('.')[-1]
				
				thumb_size = []
				
				os.rename(dir_up + x.File.filename, img_dir + new_img)
				#os.system('mv -f ' + dir_up + x.File.filename + ' ' + img_dir + new_img) #move o arquivo com o id dele
				if(thread == 0):
					thumb_size = self.thumb_gen(new_img, True)
				else:
					thumb_size = self.thumb_gen(new_img, False)
				
				img_thumb_X = thumb_size[0]
				img_thumb_Y = thumb_size[1]
				img_size = os.stat(img_dir + new_img).st_size 
				img_dim = self.gen_dim(img_dir + new_img)
				img_name = x.File.filename
			

		db.post(thread, post_id, content, usr, e_mail, "", new_img, img_name, sha1, img_thumb_X, img_thumb_Y, img_size, img_dim, usr_ip)
		return Output().pageReturnNonError("Post!")

	def pre_parsecontent(self, content):
		content = content.replace('\"', '&#34;') #this will protect the database
		content = content.replace(';', '&#59;')
		
		content = content.replace("\nThis post has been reduced.", "fag")
		
		if content.count("\n") > cut_post_lines: #cut post if it has too many lines
			lastfind = 0
			i = 0
			while i < cut_post_lines:
				lastfind = content.find("\n", lastfind+1)
				i = i+1
			content = content[0:lastfind] + "\nThis post has been reduced."
		return content
		
	def exists_in_bd(self, db, sha1):
		if(int(db.execute("SELECT count(*) FROM thread_post_t WHERE sha1=\"%s\";" % sha1)[0][0]) is 0): #image doesnt exist in db
			return False
		else:
			return True
			
	def check_is_image(self, img_file):
		is_image = False
		try:
			im = Image.open(img_file)
			is_image = True
		except Exception, e:
			is_image = False

		return is_image

	def thumb_gen(self, image_file, thread_img=True):
		im = Image.open(img_dir + image_file)
		size = new_size = im.size
		base_size = 250 #size for the op's image thumb
		
		if thread_img == False: #fix size for non-op thumb
			base_size = 125

		if (new_size[0] > base_size or new_size[1] > base_size):
			if new_size[0] >  new_size[1]: #x > y
				new_size = [base_size, ceil(float(base_size)*new_size[1]/float(new_size[0]))]
			elif new_size[1] > new_size[0]:
				new_size = [ceil(float(base_size)*new_size[0]/float(new_size[1])), base_size]
			im.thumbnail(new_size, Image.ANTIALIAS)
			im.save(img_dir + 'thumb_' + image_file)
		elif (image_file.split(".")[-1] == "gif"):
			new_size = [ceil(float(base_size-1)*new_size[0]/float(new_size[1])), base_size-1]
			im.thumbnail(new_size, Image.ANTIALIAS)
			im.save(img_dir + 'thumb_' + image_file)
		else:
			os.system("ln -s %s %sthumb_%s" % (image_file, img_dir, image_file))

		return new_size
		
	def gen_dim(self, image_file):
		im = Image.open(image_file)
		return str(im.size[0]) + 'x' + str(im.size[1])

class Output:
	def pageReturnErrorSubFolder(self, content):
		return "<html><head><link href=\"../static/yotsubanew.css\" rel=\"stylesheet\" type=\"text/css\"><META HTTP-EQUIV=\"refresh\" CONTENT=\"3; \"></head><body><center><font size=16>Error: %s</font></center></body></html>" % content
	def pageReturnErrorSubFolderRefreshBack(self, content):
		return "<html><head><link href=\"../static/yotsubanew.css\" rel=\"stylesheet\" type=\"text/css\"><META HTTP-EQUIV=\"refresh\" CONTENT=\"3; ..\"></head><body><center><font size=16>Error: %s</font></center></body></html>" % content
	def pageReturnError(self, content):
		return "<html><head><link href=\"static/yotsubanew.css\" rel=\"stylesheet\" type=\"text/css\"><META HTTP-EQUIV=\"refresh\" CONTENT=\"3; \"></head><body><center><font size=16>Error: %s</font></center></body></html>" % content
	def pageReturnNonError(self, content):
		return "<html><head><link href=\"static/yotsubanew.css\" rel=\"stylesheet\" type=\"text/css\"><META HTTP-EQUIV=\"refresh\" CONTENT=\"1; \"></head><body><center><font size=16>%s</font></center></body></html>" % content

def parsecontent(content):
	content = content.replace('<', '&#60;')
	content = content.replace('\n', '<br>')
	content = content.replace('\'', '&#39;')

	content = content.replace("This post has been reduced.", "<b>This post has been reduced.</b>")

	lines = content.split("<br>")
	for i in range(0, len(lines)):
		while lines[i].find(' ') == 0:
			lines[i] = lines[i][1:]
		if (lines[i].find(">") == 0):
			lines[i] = "<font color=\"green\">" + lines[i] + "</font>"
	
	content = lines[0]
	for i in range(1, len(lines)):
		content = content + "<br>" + lines[i]

	return content
