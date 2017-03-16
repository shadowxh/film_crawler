#!/usr/bin/env python  
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import re

proxies={"http":"http://121.232.147.66:9000","https":"http://222.217.19.242:8080",};
#proxies={"http:":"http://10.214.50.204:1080"};
urlname='http://www.dy2018.com';
film_class_cn=[u'剧情片',u'喜剧片',u'动作片',u'爱情片',u'科幻片',u'动画片',u'悬疑片',u'惊悚片',u'恐怖片',u'记录片',u'同性题材电影',u'音乐歌舞题材电影',u'传记片',u'历史片',u'战争片',u'犯罪片',u'奇幻电影',u'冒险电影',u'灾难片',u'武侠片',u'古装片',];
film_class_en=['juqing','xiju','dongzuo','aiqing','kehuan','donghua','xuanyi','jingsong','kongbu','jilu','tongxing','gewu','zhuanji','lishi','zhanzheng','fanzui','qihuan','maoxian','zainan','wuxia','guzhuang',];
all_films=[];
headers = {
		#'content-type': 'application/json',
           	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
		
}
def tag_text_is_dianzan(tag):
	return ((tag.name=='span') and (tag.string==u'点赞'));

def is_chinese(uchar):
	if uchar>=u'\u4e00' and uchar<=u'\u9fa5':return True;
	else:return False;

def do_request(url):
	time.sleep(2);
	try_times=0;
	while True:
		r=requests.get(url=url,params={},headers=headers,timeout=60);
                r.encoding='gb2312';
                if r.ok==True:break;
		try_times+=1;
		if try_times>=20:
			print r.text;
			exit();
	return r;

def get_page_count_in_a_class(class_index):
	r=do_request(urlname+'/'+str(class_index));
	soup=BeautifulSoup(r.text,'lxml');
	page_cnt=len(soup.find_all('option'));
	return page_cnt;

def error_log(message):
	err_log=open("error_log.txt","a+");
	err_log.write(message);
	err_log.close();
	return;

for class_index in range(16,len(film_class_en)):
	#get all the films in a class
	films_in_a_class=[];
	page_cnt=get_page_count_in_a_class(class_index);
	#print page_cnt;
	
	for page_num in range(1,page_cnt+1):
		print "class:",class_index,"page_num:",page_num;
		#get all the films in a page
		page_string="index";
		if page_num!=1:page_string+="_"+str(page_num);
		page_string+=".html";
		r=do_request(urlname+"/"+str(class_index)+"/"+page_string);
		soup=BeautifulSoup(r.text,'lxml');
		tbodys=soup.find_all("table");
		#print "tables in one page:",len(tbodys);
		cn=0;
		for i in range(0,len(tbodys)):
			tbody=tbodys[i];
			film_info=[];
			a_in_tbody=tbody.find_all("a");
			if len(a_in_tbody)<=1:
				err_msg="[class_index:"+str(class_index)+"page_num:"+str(page_num)+"tbody:"+str(i)+"]:no film title\n";
				#error_log(err_msg);
				continue;
			film_info=a_in_tbody[1];
			film_info=[film_info["title"],film_info["href"]];
			
			font_in_tbody=tbody.find_all("font");
                        if len(font_in_tbody)<=1:
                                err_msg="[class_index:"+str(class_index)+"page_num:"+str(page_num)+"tbody:"+str(i)+"]:no film_date or score\n";
                       		#error_log(err_msg);
				continue;
			film_date=font_in_tbody[0].string;film_date=film_date.strip();
			film_score=font_in_tbody[1].string;film_score=film_score.strip();
			film_info.extend([film_date,film_score]);
			films_in_a_class.append(film_info);#film_info=[title,href,date,score]
			cn+=1;
		print "films in one page:",cn;

	_file=open("./films/"+film_class_en[class_index],"w");
	for film in films_in_a_class:
		tmp="";
		for info in film:
			tmp+=info.encode('utf-8')+"\n";
		tmp+="\n";
		_file.write(tmp);
	_file.close();
