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
proxies={"http":"http://117.90.5.235:9000","https":"https://221.219.210.36:9000","socks5":"221.219.210.36:9000"};
domain="http://www.xicidaili.com/nn/";
url="http://www.dy2018.com";
def do_request(url):
        time.sleep(2);
        try_times=0;
        while True:
                r=requests.get(url=url,headers=headers,timeout=60);
                r.encoding='utf-8';
		#print r.text;
                if r.ok==True:break;
                try_times+=1;
                if try_times>=20:
                        print "[try too many times]:\n"+url;
                        exit();
        return r;

def test_ip(url,proxies):
	try:
		r=requests.get(url=url,proxies=proxies,headers=headers,timeout=5);
		r.encoding='gb2312';
		return True;
	except Exception as e:
		return False;

all_ip=[];
for i in range(1,2):
	r=do_request(domain+str(i));
	soup=BeautifulSoup(r.text,"lxml");
	ip_in_one_page=soup.find_all('td',text=re.compile("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"));
	print i,"  ",len(ip_in_one_page);
	for ip in ip_in_one_page:
		ip_port=ip.string.encode('utf-8');
		ip=ip.next_sibling;
		while ip.name!="td":ip=ip.next_sibling;
		ip_port+=":"+ip.string.encode('utf-8');
		all_ip.append(ip_port);

result=[];
for i in all_ip:
	if test_ip(url,{"http":i}):
		result.append(i);
		print i+" is ok";
	else:
		print i+" failed";

_file=open("ip_table.txt","w");
for i in result:_file.write(i+"\n");
_file.close();
