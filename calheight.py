'''
#=============================================================================
#     FileName: calheight.py
#         Desc: Get Height (New zeland Only)
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-04-05 23:29:58
#      History:
#=============================================================================
'''
import sys, struct
from osgeo import gdal
from osgeo import gdalconst

def getHeight_mean(Lat1,Long1,Lat2,Long2):
    minLat = float(Lat1)
    maxLat = float(Lat2)
    minLong = float(Long1)
    maxLong = float(Long2)
    dataset = gdal.Open("l10g")
    band = dataset.GetRasterBand(1)
    t = dataset.GetGeoTransform()
    success,tInverse = gdal.InvGeoTransform(t)
    if not success:
      print "Failed!"
      sys.exit(1)
    x1,y1 = gdal.ApplyGeoTransform(tInverse, minLong, minLat)
    x2,y2 = gdal.ApplyGeoTransform(tInverse, maxLong, maxLat)
    minX = int(min(x1, x2))
    maxX = int(max(x1, x2))
    minY = int(min(y1, y2))
    maxY = int(max(y1, y2))
    width = (maxX - minX) + 1
    fmt = "<" + ("h" * width)
    for y in range(minY, maxY+1):
      scanline = band.ReadRaster(minX, y,width, 1,
           width, 1,
           gdalconst.GDT_Int16)
      values = struct.unpack(fmt, scanline)
      n = 0
      mean = 0.0
      for value in values:
          mean = float((mean*n)+value)/(1+n)
          n += 1
      return mean
          

def getHeight(Lat,Long):
    minLat = float(Lat)
    maxLat = float(Lat)
    minLong = float(Long)
    maxLong = float(Long)
    dataset = gdal.Open("l10g")
    band = dataset.GetRasterBand(1)
    t = dataset.GetGeoTransform()
    success,tInverse = gdal.InvGeoTransform(t)
    if not success:
      print "Failed!"
      sys.exit(1)
    x1,y1 = gdal.ApplyGeoTransform(tInverse, minLong, minLat)
    x2,y2 = gdal.ApplyGeoTransform(tInverse, maxLong, maxLat)
    minX = int(min(x1, x2))
    maxX = int(max(x1, x2))
    minY = int(min(y1, y2))
    maxY = int(max(y1, y2))
    width = (maxX - minX) + 1
    fmt = "<" + ("h" * width)
    for y in range(minY, maxY+1):
      scanline = band.ReadRaster(minX, y,width, 1,
           width, 1,
           gdalconst.GDT_Int16)
      values = struct.unpack(fmt, scanline)
      n = 0
      mean = 0.0
      for value in values:
          return value
#print getHeight(-39.605688178320804,175.87902825325727,-39.65011210186371,175.8731231605634)
