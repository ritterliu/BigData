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

#jank_total_sec, jank_max_sec, uptime_sec, jank_per_hour_sec, freemem_mb, total_mem_mb, count
def main():
  parseFile()
  keys = []
  values_jank_total_sec = []
  values_jank_max_sec = []
  values_uptime_sec = []
  values_jank_per_hour_sec = []
  values_freemem_mb = []
  values_total_mem_mb = []
  values_count = []
  sorted_keys = sorted(FILE_content)
  for key in sorted_keys:
    value = FILE_content[key]
    values_jank_total_sec.append(value[0])
    values_jank_max_sec.append(value[1])
    values_uptime_sec.append(value[2])
    values_jank_per_hour_sec.append(value[3])
    values_freemem_mb.append(value[4])
    values_total_mem_mb.append(value[5])
    values_count.append(value[6])

  drawScatter(sorted_keys,
    values_jank_total_sec,
    values_jank_max_sec,
    values_uptime_sec,
    values_jank_per_hour_sec,
    values_freemem_mb,
    values_total_mem_mb,
    values_count)


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


def drawScatter(version,
    values_jank_total_sec,
    values_jank_max_sec,
    values_uptime_sec,
    values_jank_per_hour_sec,
    values_freemem_mb,
    values_total_mem_mb,
    values_count):
    pyplot.xlabel('version')
    pyplot.ylabel('sec')
    pyplot.title('MI6 jank jank total sec')
    pyplot.scatter(version, values_jank_total_sec)
    pyplot.show()

    pyplot.ylabel('sec')
    pyplot.title('MI6 jank jank max sec')
    pyplot.scatter(version, values_jank_max_sec)
    pyplot.show()

    pyplot.ylabel('sec')
    pyplot.title('MI6 jank uptime sec')
    pyplot.scatter(version, values_uptime_sec)
    pyplot.show()

    pyplot.ylabel('s/H ')
    pyplot.title('MI6 jank jank per hour sec')
    pyplot.scatter(version, values_jank_per_hour_sec)
    pyplot.show()

    pyplot.ylabel('MB')
    pyplot.title('MI6 jank freemem')
    pyplot.scatter(version, values_freemem_mb)
    pyplot.show()

    pyplot.ylabel('MB')
    pyplot.title('MI6 jank total mem MB')
    pyplot.scatter(version, values_total_mem_mb)
    pyplot.show()

    pyplot.ylabel('Count')
    pyplot.title('MI6 log count')
    pyplot.scatter(version, values_count)
    pyplot.show()

if __name__ == '__main__':
  print 'len(sys.argv)', len(sys.argv) 
  print '---------- sys.argv', sys.argv
  FILE_NAME = sys.argv[1]
  main()
