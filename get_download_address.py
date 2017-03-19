#encoding=utf-8
import os
import os.path
import requests
from bs4 import BeautifulSoup
import time
import re
import random
import get_ip
headers = {
	#'content-type': 'application/json',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}
proxies={"http":"106.46.136.164:808",};
domain="http://www.dy2018.com";
rootdir="./films";
ip_list=[];
ip_pointer=-1;
start_page=1;
def init_ip_list():
	global start_page,ip_list,ip_pointer,proxies;
	
	print "ip_list has been all used,so get more ip.";
	ip_list=get_ip.provide_ip(start_page);
	if len(ip_list)==0:
		print "no valid ip,will check the next page";
		start_page+=1;
		init_ip_list();
		return;
	
	proxies={"http":ip_list[0]};
	ip_pointer=0;
	return;
	
def change_ip():
	global start_page,ip_list,ip_pointer,proxies;
	if ip_pointer==(len(ip_list)-1):
		start_page+=1;
		init_ip_list();
		return;
	ip_pointer+=1;
	proxies={"http":ip_list[ip_pointer]};
	print "change ip to "+ip_list[ip_pointer];
	return;

def do_request(url):
	global proxies;
	while True:
        	try_times=0;
		try:
        		while True:
                		r=requests.get(url=url,params={},proxies=proxies,headers=headers,timeout=30);
                		r.encoding='gb2312';
                		if r.ok==True:break;
                		try_times+=1;
                		if try_times>=5:
                        		print "[try too many times]:\n"+url;
                        		return r;
			return r;
		except Exception as e:
                	change_ip();

def error_log(message):
        err_log=open("error_log.txt","a+");
        err_log.write(message+"\n");
        err_log.close();
        return;


def get_download_address(line):
	film_info=[line];
	url=domain+line;
	while True:
		r=do_request(url);
		soup=BeautifulSoup(r.text,'lxml');
		zoom=soup.find_all(id='Zoom');
		if r.ok==False:
			return film_info;
		if len(zoom)==0:
			print "can't find zoom,retry..."
			continue;
		break;
	
	zoom=zoom[0];
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
	init_ip_list();
	for file_name in files:
		if ".link" in file_name:continue;
		print file_name;
		links_in_a_file=[];
		_file=open(os.path.join(parent,file_name),"r");
		for line in _file:
			if line[0:3]=="/i/":continue;
			if (line[-6:-1]!=".html") and (line[-5:-1]!=".php"):continue;
			links_in_a_file.append(line[:-1]);
		_file.close();
		
		_file=open(os.path.join(parent,file_name+'.link'),"a+");
		for link in links_in_a_file:
			info=get_download_address(link);
			if len(info)<=1:
				print "try "+link+" too many times,give up.";
				error_log(link+" giveup");
			for i in info:
				_file.write(i+"\n");
		
		_file.close();

