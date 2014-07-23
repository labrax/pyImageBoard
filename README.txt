pyImageBoard

Features
CHANGELOG
Packages required
Note to use
Mysql
Additional Files

Bugs/todo: https://docs.google.com/document/d/1obGbqJs2_fSZdz1UjTccYBQunWQyx-FnxgNcQvMnHZ4/edit?usp=sharing

Features:
	-simple imageboard with homepage and threadpage
	-layout from 4chan
	homepage:
		-display all threads with 2 last posts
		-display counter of replies and image replies
	thread page:
		-display all posts
	op post:
		-image needed
		-also ref posts
	posts:
		-display general info
		-link e-mail (if added)
		-parse text: reduce content, remove ", remove html-tags, add greentext
		-with or without image
		-sage (doesnt bump thread)
	thumbs:
		-op image is scalated with maximum size 250x250
		-post image is scalated with maximum 125x125
		-generated with thumb_%img_id name in ./src/ (if needed)
	system:
		-2 tables with duplicate image protection (sha1)
		-post and image individual counters
		-image temporary saved in ./temp/ and then moved with its individual name to ./src/
		-when asking for a file and is not found returns 'something_ww.jpg'
		-recreate.py to recreate database and delete image files
		-cache (images and pages)
		-ip record on post_table
		-anti flooding by ip address

CHANGELOG:
	0.903:
	        -cache of images in http header now works
        	-reduce of code and config file
	        -images now are directly loaded from lighttpd
		-fix on gen_bkp.bash
	0.902:
		-gifs thumb isnt animated anymore
		-migration to mysql
		-mysql migration bug correction
		-added config file from lighttpd to source diretory as bkp
		-migration of folders
		-code changes and cleanup
		-backup script
		-fix drop_tables in dbconn to delete the images
	0.901:
		-minor programming mistakes
		-table
		-changed hash to sha1
		-statistics within admin tools
	0.9:
		-cache upgraded to a smarter one
		-ip record on post_table
		-anti flooding with 10s wait time (based on ip, disabled)
		-begin of admin tools file
	0.8:
		-sage
		-cache

Packages required:
	- python-webpy
	- python-imaging
	- python-mysqldb
	- python-fcgi
	- mysql-server
	- lighttpd
	- ligghtpd-fastcgi

Note to use:
	- to use set the password in the dbconn.py.no_pass file and rename to dbconn.py
	- test the server with python main.py
	- fix permissions with chmod
	- run the server with the lighttpd config file

MySql:
	-To login:
		$ mysql --user=root --password=PASS
	-To create database:
		CREATE DATABASE mydb;
	-To select database:
		USE mydb;
	-Create tables using dbconn.DbConn();

Additional Files:
	-There are needed files to fill the /static/ folder. They are:
	4chan_favicon.ico: 16x16
	banner.jpg: 300x100
	fade.png: 1x200
	favicon.ico: 16x16
	yotsubanew.css
