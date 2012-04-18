import sys, struct
from osgeo import gdal
from osgeo import gdalconst
minLat = -45.74452698046842
maxLat = -45.74452698046842
minLong = 169.95849609375
maxLong = 169.95849609375
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
  for value in values:
	  print value
