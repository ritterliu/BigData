#!/usr/bin/env python
# coding = utf-8
import json
import sys
from matplotlib import pyplot

FILE_NAME = ''

FILE_content = {}

#  avg_total_duration,
#  avg_uptime,
#  avg_max_frame_duration,
#  avg_tmem,
#  count,
#  avg_jank_per_hour)
#7.9.25-internal, MI 6 , 2010.85 MB, 359.27  s, 28751.27 s, 217.77  s, 6.00 GB, 3046 , 44.98 s/h
def parseFile():
  fileContent = open(FILE_NAME,'r').readlines()
  for line in fileContent:
    infos = line.split(',')
    version = infos[0].strip()
    model = infos[1].strip()
    freemem_mb = (float)(infos[2].strip().split(' ')[0])
    jank_total_sec = (float)(infos[3].strip().split(' ')[0])
    jank_max_sec = (float)(infos[5].strip().split(' ')[0])
    uptime_sec = (float)(infos[4].strip().split(' ')[0])
    total_mem_mb = (float)(infos[6].strip().split(' ')[0])
    count = (int)(infos[7].strip())
    jank_per_hour_sec = (float)(infos[8].strip().split(' ')[0])
    print 'line:', line
    print 'version:', version
    print 'model:', model

    if isVersionAllow(version):
      FILE_content[formatVersion(version)] = [jank_total_sec, jank_max_sec, uptime_sec,
      jank_per_hour_sec, freemem_mb, total_mem_mb, count]
    
  print '-----------FILE_content:', FILE_content


def main():
  parseFile()
  keys = []
  values_jank_per_hour_sec = []
  values_freemem_mb = []
  sorted_keys = sorted(FILE_content)
  for key in sorted_keys:
    value = FILE_content[key]
    values_jank_per_hour_sec.append(value[3])
    values_freemem_mb.append(value[4])
    print '%d:%d',(key,FILE_content[key][3])

  drawScatter(sorted_keys, values_jank_per_hour_sec, values_freemem_mb)


def formatVersion(ver):
  vers = ver.split('.')
  print 'vers:', vers
  year = vers[0]
  month = vers[1]
  day = vers[2]
  print 'year:', year
  print 'month:', month
  print 'day:', day
  if len(month) < 2:
    month = '0' + month

  if len(day) < 2:
    day = '0' + day
  return (year + '.' + month + '.' + day)

def isVersionAllow(version):
  print 'isVersionAllow version:', version
  if len(version) > 7:
    return False

  vers = version.split('.')
  year = (int)(vers[0])
  month = (int)(vers[1])
  day = (int)(vers[2])
  if month < 1 or month > 12:
    return False

  if day < 1 or day > 31:
    return False
  return True


def drawScatter(version, values_jank_per_hour_sec, values_freemem_mb):
    pyplot.xlabel('version')
    pyplot.ylabel('values')
    pyplot.title('MI6 jank report')
    pyplot.scatter(version, values_jank_per_hour_sec)
    pyplot.show()
    pyplot.scatter(version, values_freemem_mb)  
    pyplot.show()



if __name__ == '__main__':
  print 'len(sys.argv)', len(sys.argv) 
  print '---------- sys.argv', sys.argv
  FILE_NAME = sys.argv[1]
  main()
