#!/bin/bash

if [ $1 ]; then
   if [ ! -f /bkp/imageboard$1.tar.gz ]; then
       if [ "${2}" = "del" ]; then
          (cd cgi-bin && python recreate.py);
          echo "DELETED DATABASE";
       fi

       if [ "${2}" = "copy" ]; then
           #copy data to server    
           scp -r cgi-bin/ root@webserver:/var/www > /dev/null;
           echo "COPIED DATA TO SERVER";
       fi

       #cp /etc/lighttpd/lighttpd.conf lighttpd.conf.bkp
       if [ "${2}" = "copy" ]; then
           scp root@webserver:/etc/lighttpd/lighttpd.conf lighttpd.conf.bkp > /dev/null;
           echo "COPIED CONFIG FROM SERVER";
       fi

       rm cgi-bin/*.pyc
       rm -f cache/*

       sed '12s/.*/password = /' cgi-bin/dbconn.py > cgi-bin/dbconn.py.no_pass
       tar --exclude=bkp --exclude=cgi-bin/dbconn.py -cjf bkp/imageboard$1.tar.gz *;
       echo -e "CHECK IF PASSWORD IS STILL IN SOURCE CODE:\e[0;31m"
       cat cgi-bin/dbconn.py.no_pass | grep "password ="
       echo -e "\e[0mCHECK ABOVE"
       rm cgi-bin/dbconn.py.no_pass
       echo "Created with name imageboard$1.tar.gz"
   fi
fi

if [ ! $1 ]; then
	echo "\
		Use as ./bkp.bash <version_code>
		If you want to recreate the tables and delete the images use as:
		
		./bkp.bash <version_code> del"
fi
