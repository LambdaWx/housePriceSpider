# -*- coding: utf-8 -*-
"""
@author: zbc
"""
import os
import tornado.ioloop
import tornado.httpserver
import tornado.web
import json
import math
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

''''
生成hotregin
'''
def _mkF( sf ):
    vf = round( float(sf), 9 )
    return vf

def _loadLocations(filename):
    if filename== None:return
   
    filen = filename
    hd = file( filen, "r" )
    if not hd: return [ [0,[] ], [] ]
    pts = []
    for line in hd:
        ay = line.strip().split(",")
        if len( ay ) < 6: continue
        pts.append( [ ay[4], ay[3], ay[5] ] )
    hd.close()
    hotRegion =  _loadPts( pts )
    return hotRegion

def _loadPts( fpts ):
    d = {}
    #print len(fpts)
    for ay in fpts:
        if len( ay ) != 3: continue
        try:
            latf = _mkF( ay[0] )
            lotf = _mkF( ay[1] )
            r =  [ latf, lotf ]
            k = "%f %f"%(  r[0], r[1] )
            d[k] = [ r, int(ay[2]) ]
        except:pass

    #print len(d)
    if len( d ) == 0: return [ 0, [] ]

    dd = []
    for k in d: dd.append( d[k] )

    len1 = len(dd)
    dd = sorted( dd, key=lambda x:x[1], reverse = True )
    sz = min( 50000, len1 )
    dd = dd[0: sz ]
        
    ret = []
    maxv = 0
    minv = 10000
    array = []
    i = 0
    for k in dd:
        r = k[0]
        c = k[1]
        c = int( round( math.log( c, 4 ) + 4, 0 ) )
        array.append({"lng": r[1],"lat":r[0], "count": c*10})
        i = i + 1

    return array
"""
def _loadUserPts( fpts ):
    d = {}
    #print len(fpts)
    for ay in fpts:
        if len( ay ) != 2: continue
        try:
            latf = _mkF( ay[0] )
            lotf = _mkF( ay[1] )

            r =  [ latf, lotf ]
            k = "%f %f"%(  r[0], r[1] )
            #print k
            if k not in d:
                d[k] = [ r, 1 ]
            else:
                d[k][1] = d[k][1] + 1
        except:pass

    #print len(d)
    if len( d ) == 0: return [ 0, [] ]

    dd = []
    for k in d: dd.append( d[k] )

    len1 = len(dd)
    dd = sorted( dd, key=lambda x:x[1], reverse = True )
    sz = min( 50000, len1 )
    dd = dd[0: sz ]
        
    ret = []
    maxv = 0
    minv = 10000
    array = []
    i = 0
    for k in dd:
        r = k[0]
        c = k[1]
        c = int( round( math.log( c, 4 ) + 4, 0 ) )
        array.append({"lng": r[1],"lat":r[0], "count": c*10})
        i = i + 1

    return array
"""       
map_center = {"chengdu":[30.67, 104.064],"beijing":[39.9772370000,116.3959960000],"shanghai":[31.236305,121.480237]}
map_level = {"chengdu":13,"beijing":12,"shanghai":12}

class orderClusterHandler(tornado.web.RequestHandler):
    def get(self):
        if True : 
            mapCentor = [30.67, 104.064]
            mapLevel = 14
            filename = "../chengdu.txt"
            #热点数据
            hot_regin = _loadLocations(filename)
            self.render( "hotregion.template.html", 
                        center_lon=mapCentor[1], center_lat=mapCentor[0], 
                        hotregin=hot_regin)

def make_app():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path":os.path.join(os.path.dirname(__file__), "src"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        }    

    return tornado.web.Application(handlers=[ (r"/", orderClusterHandler),
        ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8110)
    tornado.ioloop.IOLoop.current().start()
