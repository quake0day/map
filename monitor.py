# -*- coding: utf8 -*-
import subprocess
import os
import sys
import time
from time import sleep
import MySQLdb
import random
import shutil
from conn import connMysql
from caldistance import CalDis
from getPathLossExp import read_data
from getPathLossExp import getPathLossExp
from loadc import getConductivity
from trim import trim
from txt2image import txt2image
from txt2html import plaintext2html
import getHeight
from getHeight import getPathInfo
from getHeight import formatPathInfo
from getHeight import getHTT
from getHeight import getHRR
from millinton import cal_milliton
from upyun import UpYun,md5,md5file

MIN_POINT = 2
TRACE_FILE_NAME = "simple.tr"
def get_job():
    conn = connMysql()
    cur = conn.cursor()
    sql = "SELECT * FROM `main` WHERE `status`=0 LIMIT 0,30"
    cur.execute(sql)
    dataset = cur.fetchall()
    cur.close()
    conn.close()
    return dataset

def split_job(dataset):
    jobs={}
    for data in dataset:
        jobs.setdefault(data[1],[]).append(data)
    for job in jobs:
        yield list(jobs.get(job,()))

def do_simulation(job):
    # for DEBUG
    try:
        running_id = job[0][1]
        lat1 = job[0][2]
        lat2 = job[0][4]
        lng1 = job[0][3]
        lng2 = job[0][5]
        freq = int(job[0][11])
        pol = int(job[0][12])
        height = float(job[0][13])
        height_r = float(job[0][14])
        bandwidth = float(job[0][15])
    except Exception,e:
        print "ERROR- Point Num ERROR OR Lack LAT LNG"
        mark_as_complete(job[0])
        return 1
    #save_res(show_res("out"),job[0])
    try:
        dis = CalDis(lat1,lng1,lat2,lng2)
    except Exception,e:
        print "error cal dis"
        mark_as_complete(job[0])
    try:
        con1 = getConductivity(lat1,lng1)
    except Exception,e:
        print "error cal con1"
        mark_as_complete(job[0])
    try:
        geo_height = getPathInfo(running_id)
        #print geo_height
        if geo_height == None:
            raise Exception,e
    except Exception,e:
        print "cannot grab geo_info"
        mark_as_complete(job[0])
    try:
        geo_height2 = formatPathInfo(geo_height)
        #print geo_height2
    except Exception,e:
        mark_as_complete(job[0])
        print "geo height grab error"
        print geo_height
        return 1
    try:
        #hei1_mean = getHeight_mean(lat1,lng1,lat2,lng2)
        HTT = getHTT(geo_height2) + height
        HRR = getHRR(geo_height2) + height_r
        print "HTT:",HTT,HRR
    except Exception,e:
        print "error cal HTT HRR"
        mark_as_complete(job[0])
        return 1
    try:
        res =\
        cal_milliton(geo_height2,int(freq),int(pol),dis,HTT,HRR,height,height_r)
        if res is not None:
            save_Et(res,job[0])
    except Exception,e:
        print e
        mark_as_complete(job[0])
        return 1
    try:
        fp = open("inp","w")
    except Exception,e:
        print "error open"
    command1 = "HTT {} \n\
               HRR {} \n\
               IPOLRN {}\n\
               FREQ {} \n\
               SIGMA {} \n\
               EPSLON 30 \n\
               dmin 1\n\
               dmax {}\n\
               dstep 5\n\
               GO\
               ".format(str(HTT),str(HRR),pol,freq,con1,dis)
    fp.write(command1)
    fp.close()
    fp = open("inp2","w")
    command = "HTT {} \n\
               HRR {} \n\
               IPOLRN {}\n\
               FREQ {} \n\
               SIGMA {} \n\
               EPSLON 30 \n\
               dmin 1\n\
               dmax 1000\n\
               dstep 5\n\
               GO\
               ".format(str(HTT),str(HRR),pol,freq,con1)
    fp.write(command)
    fp.close()
#    except Exception,E:
#        print command1
#        print "Error writing inp inp2"
        #return 1
    # running grwave the result will save in out
    rungrwave=os.getcwd()+"/gr <inp >out"
    rungrwave_for_ns2=os.getcwd()+"/gr <inp2 >out2"
    runget_result="sh "+os.getcwd()+"/get_res.sh"
    run_get_KM = "perl get_KM.pl out2 > KM"
    run_get_BPL = "perl get_BasicPathLoss.pl out2 > BPL"
    run_ns2 = os.getcwd()+"/ns dsr.tcl "
    try:
        process1 = subprocess.Popen(rungrwave,shell=True)
        process1.wait()
    except Exception,E:
        print "Error process 1"
        mark_as_complete(job[0])
        return 1
    try:
        process2 = subprocess.Popen(rungrwave_for_ns2,shell=True)
        process2.wait()
    except Exception,e:
        print "Error process 2"
        mark_as_complete(job[0])
        return 1
    try:
        process3 = subprocess.Popen(run_get_KM,shell=True)
        process3.wait()
    except Exception,E:
        print "Error process 3"
        mark_as_complete(job[0])
        return 1
    try:
        process4 = subprocess.Popen(run_get_BPL,shell=True)
        process4.wait()
    except Exception,E:
        print "Error process 4"
        mark_as_complete(job[0])
        return 1
    try:
        DAT_KM = read_data("KM")
        DAT_BPL = read_data("BPL")[3:]
    except Exception,E:
        print "Error process read data"
        mark_as_complete(job[0])
        return 1
    try:
        PathLossExp = getPathLossExp(DAT_KM,DAT_BPL)
    except Exception,e:
        print "Error get pathlossexp"
        req0 = mark_as_complete(job[0])
        return 1
    try:
        bandwidth_ns = " " + str(bandwidth)+"bps"+ " "
        freq_ns = " "+str(freq)+"e6"+" "
        dis_ns = " "+str(dis*1000)+" "
        run_ns2 = run_ns2+str(0.1)+bandwidth_ns+freq_ns+dis_ns
        print run_ns2
        process = subprocess.Popen(run_ns2,shell=True)
        process.wait()
    except Exception,e:
        print "run_ns2 error"
        mark_as_complete(job[0])
    try:
        run_ana_throughput = "perl mea.pl "+TRACE_FILE_NAME
        process_out =\
        subprocess.Popen(run_ana_throughput,stdout=subprocess.PIPE,shell=True).communicate()
    except Exception,e:
        print "run_ana_throughput error"
    print process_out[0]
    print len(process_out[0].split(","))
    save_res(process_out[0],"throughput",job[0])

    try:
        run_ana_del = "perl del.pl "+TRACE_FILE_NAME
        process_out =\
        subprocess.Popen(run_ana_del,stdout=subprocess.PIPE,shell=True).communicate()
    except Exception,e:
        print "run_ana_del error"
        mark_as_complete(job[0])
    print process_out[0]
    print len(process_out[0].split(","))
    save_res(process_out[0],"delay",job[0])
    
    try:
        random_num = upload_res()
    except Exception,e:
        mark_as_complete(job[0])
        print "upload res error"
        return 1
    try:
        save_res(random_num,"res",job[0])
    except Exception,e:
        mark_as_complete(job[0])
        print "save res error"
        return 1
    #K = subprocess.Popen(runget_result,shell=True,stdout=subprocess.PIPE)
    req0 = mark_as_complete(job[0])
    #save_res(show_res("out"),job[0])
    #print show_res("out")

def show_res(file):
    fout = open(file,"r")
    return fout.read()

def save_res(data,name,task):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `"+name+"` = \""+data+"\" where running_id= " +str(task[1])
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close
    conn.close()

def save_Et(Et,task):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `Et` = "+str(Et)+" where running_id="+\
            str(task[1])
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def upload_res():
    random_num = str(random.randrange(0,10001,2))
    try:
		#u = UpYun('groundwave','quake0day','mZy0rJGP')
		#data = open(os.getcwd()+"/out",'r')
		#data_tr = open(os.getcwd()+"/simple.tr",'r')
		#a = u.writeFile(random_num+".txt",data)
		#b = u.writeFile("/tr/"+random_num+".txt",data_tr)
		#print random_num
        shutil.copy2(os.getcwd()+"/out","/home/quake0day/www/res/"+random_num)
        shutil.copy2(os.getcwd()+"/simple.tr","/home/quake0day/www/tr/"+random_num)
    except Exception,e:
        print "upload error"
    return random_num

def save_res_plot(res,task):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `throughput` =\""+res+"\" where running_id=\
    "+str(task[1])
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 0

def mark_as_complete(task):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `status` = 1 where running_id= " +str(task[1])
   # print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 0
if __name__ == '__main__':
    while 1:
        sleep(1)
        try:
            job = split_job(get_job())
        except Exception,e:
            pass
        try:
            do_simulation(job.next())
            sleep(1)
        except Exception,e:
            pass
