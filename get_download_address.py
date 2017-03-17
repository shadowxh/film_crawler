#encoding=utf-8
import os
import os.path
import requests
from bs4 import BeautifulSoup
import time
import re
import random
headers = {
	#'content-type': 'application/json',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}
proxies={"http","http://192.118.72.53:80"};
domain="http://www.dy2018.com";
rootdir="./films";

def do_request(url):
	sleep_time=2+2*random.random();
        time.sleep(sleep_time);
        try_times=0;
        while True:
                r=requests.get(url=url,params={},headers=headers,timeout=60);
                r.encoding='gb2312';
                if r.ok==True:break;
                try_times+=1;
                if try_times>=20:
                        print "[try too many times]:\n"+url;
                        exit();
        return r;

def error_log(message):
        err_log=open("error_log.txt","a+");
        err_log.write(message+"\n");
        err_log.close();
        return;

def has_attr_thunderpid(tag):
	return (tag.name=='a') and (tag.has_attr('thunderpid'));

def get_download_address(line):
	film_info=[line[3:-5]];
	url=domain+line;
	r=do_request(url);
	soup=BeautifulSoup(r.text,'lxml');
	zoom=soup.find(id='Zoom');
	imgs=zoom.find_all('img');
	film_info.append(str(len(imgs)));
	for img in imgs:
		film_info.append(img['src'].encode('utf-8'));
	download_links=zoom.find_all(text=re.compile(".*ftp:.*"));
	film_info.append(str(len(download_links)));
	for link in download_links:
		film_info.append(link.string.encode('utf-8'));
	
	print line,len(imgs),len(download_links);
	if (len(imgs)<2) or (len(download_links)==0):
		error_log(line+" "+str(len(imgs))+" "+str(len(download_links)));
	return film_info;
	
for parent,dirs,files in os.walk(rootdir):
	for file_name in files:
		print file_name;
		links_in_a_file=[];
		_file=open(os.path.join(parent,file_name),"r");
		for line in _file:
			if line[0:3]!="/i/":continue;
			links_in_a_file.append(line[:-1]);
		_file.close();
		
		_file=open(os.path.join(parent,file_name+'.link'),"w");
		for link in links_in_a_file:
			info=get_download_address(link);
			for i in info:
				_file.write(i+"\n");
		
		_file.close();

