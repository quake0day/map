import MySQLdb
import re
from conn import connMysql

def getPathInfo(running_id):
    conn = connMysql()
    cur = conn.cursor()
    sql = "select path_info FROM `main` where `running_id` ="+str(running_id)+\
            " order by id desc"
    cur.execute(sql)
    path_info = cur.fetchone()
    cur.close()
    conn.close()
    return path_info

def formatPathInfo(path_info):
#    print path_info
    data = path_info[0]
    data1 = data.split("(")
    geo_height = []
    for item in data1:
        if item != "":
            latlng = item.split("),")[0].split(",")
            height = item.split("),")[-1].split(",")
            dataset = [latlng[0],latlng[1],height[0]]
            geo_height.append(dataset)
    return geo_height
            

def getHTT(geo_height):
    return geo_height[0][2]

def getHRR(geo_height):
    return geo_height[-1][2]

#geo = formatPathInfo(getPathInfo("15"))
#print geo
#print getHRR(geo)

