# -*- coding: utf-8 -*-
import json
import re
import io
import datetime
import random
import time
import urllib
import urllib2
import pymongo
import datetime
import time
import sys
import demjson
from bs4 import BeautifulSoup
from math import *
reload(sys)
sys.setdefaultencoding( "utf-8" )

# input Lat_A 纬度A
# input Lng_A 经度A
# input Lat_B 纬度B
# input Lng_B 经度B
# output distance 距离(km)
def calcLatLngDist(Lat_A, Lng_A, Lat_B, Lng_B, Debug = False ):
    Lat_A = float(Lat_A)
    Lng_A = float(Lng_A)
    Lat_B = float(Lat_B)
    Lng_B = float(Lng_B)
    #print Lat_A, Lng_A, Lat_B, Lng_B
    if Lat_A == Lat_B and  Lng_A ==  Lng_B: 
		if Debug: print "_calcLatLngDist return as equal"
		return 0

    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    distance = 0
    try:
    	xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
        c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
       	distance = ra * (xx + dr)
    except  Exception,e:
	if Debug: 
		print "_calcLatLngDist return as exception:"
		print Lat_A, Lng_A, Lat_B, Lng_B
		print e
        return 0
    return distance
calcLatLngDist(104.131182,30.655364, 104.06, 30.67)  
 
def getGdLocation(address):
    try:
        #Key名称:adrDev249091488
        Key = '48bdf4f06248826b22e51538dccb5f4d'
        appKeys = ['7ba215f6db353d2aa66c55fa4dfe99ad','b80ccd147375ed37bfbdd9025ed9e384','5a9a676d40a02bbcf3cbe2bc581f0e26','7c046c20b0e2c70020d39b4988116127','74182609e8238c9822282985734ed495','595db8b17bed1ad220b79ff08e3fedaa','701dc8acd6d7aec627c678623f40f861','af2dd94fee5153f44d4e34160a4fdbe7','f51c07f0b4cecf5a773a63c87099645c','9f566db560bd026c506e1efaa75c3952','44379632a8984fb7d5d88f7d9bf6e5b2']
        rdOff = random.randint( 0, len( appKeys ) - 1 )
        appK = appKeys[rdOff]        
        gdUrl = 'http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&city=成都'%(appK,address)
        req = urllib2.Request( gdUrl )
        data = urllib2.urlopen( req )
        res = data.read()
        res = json.loads( res )
        if res and res['info'] == 'OK' and 'geocodes' in res and len(res['geocodes'])>0 and 'location' in res['geocodes'][0]:
            location = res['geocodes'][0]['location']
            city = res['geocodes'][0]['city']
            district = res['geocodes'][0]['district']
            return location,city,district
        else:
            print res
            return None,"",""
    except:
        return None,"",""
        
appKeys = [ "4032f6db1085b0c63683ef3917e40428","IkSvwkWPwCuICyAjnS0QGBzw","6WDQYk8GK6CbusVvepkSQKST","CvbddAko7nt1layAy2IPYuZe", "0ufxKGZM4j0dyzwK7FF6fS5L", "Ni07CGCmkAiRCtCTcq1rql4B","tnPseOMpG3G02Rk5pWN2NXBt","Weefu0Q7Lj6BTdVLkHYEonQo" ]
def getBdLocation(address):
    try:
        rdOff = random.randint( 0, len( appKeys ) - 1 )
        appK = appKeys[rdOff]
        urlAddress = "http://api.map.baidu.com/geocoder?address=%s&output=json&key=%s"%( name, appK)
        req = urllib2.Request( urlAddress )
        data = urllib2.urlopen( req )
        res = data.read()
        res = json.loads( res )
        lat = -1
        lng = -1
        if res and res['status'] == 'OK' and ('result' in res and 'location' in res['result'] and 'lng' in res['result']['location']): 
            lng = res['result']['location']['lng']
            lat = res['result']['location']['lat']
            location =  'lng:%s,lat:%s'%(lng,lat)   
            return location
        else:
            print res
            return None
    except:
        return None
cityList = ["成都"]

fw = open("./chengdu.txt","a+")
index = [i+1 for i in range(32)]
for pa in index:  
    try:
        if pa==1:
            url = "http://cd.fang.lianjia.com/loupan/"
        else:
            url = "http://cd.fang.lianjia.com/loupan/pg%d/"%(pa)
        print "request:"+url
        req = urllib2.Request( url )
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
        req.add_header("Accept","*/*")
        req.add_header("Accept-Language","zh-CN,zh;q=0.8")
        
        data = urllib2.urlopen( req )
        res = data.read()
        #print res
        #res = res.replace("&nbsp;","")
        #print res
        #objects = demjson.decode(res)
        
        soup = BeautifulSoup(res)
        houseLst = soup.findAll(id='house-lst')
        resp = soup.findAll('div', attrs = {'class': 'info-panel'})
        
        for i in range(len(resp)):
            name =  resp[i].findAll('a', attrs = {'target': '_blank'})[0].text 
            
            privice = resp[i].findAll('span', attrs = {'class': 'num'})
            privice =  privice[0].text
             
            region = resp[i].findAll('span', attrs = {'class': 'region'})
            address =  region[0].text.split('（')[0]
            ##解析获得经纬度
            location,city,district = getGdLocation(name)
            if not location:
                location = getBdLocation(address)#自定义函数
            if not location:
                continue
            formatStr = "%s,%s,%s,%s,%s\n"%(city,district,name,location,privice)
            print formatStr
            fw.write(formatStr)
    except:
        pass
fw.close()

            
#二手房数据获取
fw = open("./chengdu2.txt","a+")
index = [i+1 for i in range(100)]
for pa in index:  
    try:
        if pa==1:
            url = "http://cd.lianjia.com/ershoufang/"
        else:
            url = "http://cd.lianjia.com/ershoufang/pg%d/"%(pa)
        print "request:"+url
        req = urllib2.Request( url )
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
        req.add_header("Accept","*/*")
        req.add_header("Accept-Language","zh-CN,zh;q=0.8")
                
        data = urllib2.urlopen( req )
        res = data.read()
                
        soup = BeautifulSoup(res)
        resp = soup.findAll('div', attrs = {'class': 'content'})
        resp = resp[0].findAll('ul', attrs = {'class': 'sellListContent'})
        resp = resp[0].findAll('li', attrs = {'class': 'clear'})
        for i in range(len(resp)):
            address = resp[i].findAll('div', attrs = {'class': 'address'})
            address = address[0].findAll('a', attrs = {'target': '_blank'})[0].text 
            address = address.replace(" ","")
            
            addressAddInfo = resp[i].findAll('div', attrs = {'class': 'positionInfo'})[0].findAll('a', attrs = {'target': '_blank'})[0].text
            name = address
            address = address +"_" + addressAddInfo
            
            print address
            unitPrice = resp[i].findAll('div', attrs = {'class': 'unitPrice'})[0].text
            unitPrice =  unitPrice.replace("单价","").replace("元/平米","")
            ##解析获得经纬度
            ##售房者填写的地址和楼盘名字可能有误，通过楼盘和区域名来获取经纬度的同时，验证其可靠性
            location = None
            location1,city,district = getGdLocation(name)
            location2,city,district = getGdLocation(address)
            if location1 and location2:
                distince = calcLatLngDist(location1.split(',')[0], location1.split(',')[1], location2.split(',')[0], location2.split(',')[1])
                print distince
                if distince > 6.0:
                    continue
                print "distince验证通过：%s"%(distince)
                distince1 = calcLatLngDist(location1.split(',')[0], location1.split(',')[1], 104.06, 30.67)
                distince2 = calcLatLngDist(location2.split(',')[0], location2.split(',')[1], 104.06, 30.67)
                if distince1 < distince2:
                    location = location1
                else:
                    location = location2
            if not location:
                location = getBdLocation(address)
            if not location:
                print "地址解析失败"
                continue
            formatStr = "%s,%s,%s,%s,%s\n"%(city,district,name,location,unitPrice)
            print formatStr  
            fw.write(formatStr)
    except:
        pass
fw.close() 


















