#!/usr/bin/env python
# coding = utf-8
import json
import sys
import pickle
from matplotlib import pyplot

FILE_NAME = ''

LAUNCH_TIME_DICT= {}

TOP_LAUNCH_COUNT_APP = [
"com.android.settings/.SubSettings",
"com.android.mms/.ui.SingleRecipientConversationActivity",
"com.miui.securitycenter/com.miui.wakepath.ui.ConfirmStartActivity",
"com.android.browser/.BrowserActivity",
"com.tencent.mm/.plugin.profile.ui.ContactInfoUI",
"com.tencent.mm/.ui.chatting.gallery.ImageGalleryUI",
"com.tencent.mm/.plugin.setting.ui.setting.SettingsUI",
"com.tencent.mm/.ui.chatting.SendImgProxyUI",
"com.tencent.mobileqq/.activity.photo.PhotoPreviewActivity",
"com.tencent.mobileqq/.activity.aio.photo.AIOGalleryActivity",
"com.eg.android.AlipayGphone/com.alipay.mobile.homefeeds.morecards.HomeMoreCardsActivity",
"com.eg.android.AlipayGphone/com.alipay.mobile.nebulacore.ui.H5Activity"
]

def parseFile():
  fileContent = open(FILE_NAME,'r').readlines()
  for line in fileContent:
    infos = line.split('{\"launch_time\"')
    print '-----------infos:', infos

    version = formatVersion(infos[0].split('\t')[0])
    model = infos[0].split('\t')[1]

    # launch_json = json.load('{\"launch_time\"' + infos[1])

    launch_json = byteify(json.loads('{\"launch_time\"' + infos[1]))
    print '-----------launch_json:', launch_json
    print '-----------launch_json[launch_time]:', launch_json['launch_time']
    print '-----------model version:', model, version
    launch_time_json = launch_json['launch_time']

    for pkg,launch_time_list in launch_time_json.items():
        print 'pkg:', pkg
        print 'launch_time_list:', launch_time_list
        launch_time_json[pkg] = launch_time_list

    storeIntoDict(model, version, launch_time_json)
    saveFile()


def saveFile():
    f1 = open('LAUNCH_TIME_DICT.txt','wb')
    pickle.dump(LAUNCH_TIME_DICT, f1)
    f1.close()

def readFile():
    f2 = open('LAUNCH_TIME_DICT.txt','rb')
    dict_content = pickle.load(f2)
    f2.close()
    return dict_content

def storeIntoDict(model, version, launch_time_dict):
    new_key = (model + ':' + version)
    if LAUNCH_TIME_DICT.has_key(new_key):
        appendLaunchTimeDict(launch_time_dict, LAUNCH_TIME_DICT[new_key])
    else:
        LAUNCH_TIME_DICT[new_key] = launch_time_dict


def appendLaunchTimeDict(source, destination):
    for pkg,avg_launch_time in source.items():
        if destination.has_key(pkg):
            launch_time_list = (destination[pkg] + avg_launch_time)
            destination[pkg] = launch_time_list
        else:
            destination[pkg] = avg_launch_time


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def drawByModel(model, launch_time_dict):
    version_list = []
    avg_launch_time_list = []
    pic = 0

    sorted_version = sorted(launch_time_dict.keys())
    # print 'sorted_version:', sorted_version 

    for app in TOP_LAUNCH_COUNT_APP:
        pic = pic + 1
        for k, v in launch_time_dict.items():
            if k.startswith(model):
                version = formatVersion(k.split(':')[1])
                if k not in version_list:
                    version_list.append(k)

                #print 'len(v):', len(v)
                if app in v.keys():
                    #print 'ver:', k , ' v.has_key:', app
                    avg_launch_time_list.append(calculateAVGLaunchTime(v[app], app))
                else:
                    #print 'ver:', k , ' v.not has_key:', app
                    avg_launch_time_list.append(-1)

        #print 'version_list:', version_list
        print 'APP:', app, '  avg_launch_time_list:', avg_launch_time_list
        # ax = pyplot.subplots()
        pyplot.plot(version_list, avg_launch_time_list,
            marker='o', label=app)
        # pyplot.legend(loc='SouthOutside', bbox_to_anchor=(0.0,0.0),ncol=1,fancybox=True,shadow=True) 
        pyplot.legend(loc='best', ncol=1) 
        avg_launch_time_list = []

#plt.plot(x, y, marker='o', mec='r', mfc='w',label=u'y=x^2')
#plt.plot(x, y1, marker='*', ms=10,label=u'y=x^')

        if pic%6 == 0 or pic == len(TOP_LAUNCH_COUNT_APP):
            pyplot.subplots_adjust(bottom=0.15)
            pyplot.xlabel('Version')
            pyplot.ylabel('ms')
            pyplot.title('Avg launch time')
            pyplot.show()


def formatVersion(ver):
  vers = ver.split('.')
  year = vers[0]
  month = vers[1]
  day = vers[2]
  if len(month) < 2:
    month = '0' + month

  if len(day) < 2:
    day = '0' + day
  return (year + '.' + month + '.' + day)

def calculateAVGLaunchTime(launch_time_list, app):
    count = 0
    total = 0
    for item in launch_time_list:
        if item < 5000:
            total = total + item
            count = count + 1
        else:
            print '!!!---', app, ' > 5000, item:', item
    if count == 0:
        return 0
    return (int)(total/count)

def draw():
  LAUNCH_TIME_DICT = readFile()
  print 'LAUNCH_TIME_DICT:', LAUNCH_TIME_DICT
  drawByModel('MI 6', LAUNCH_TIME_DICT)
  drawByModel('MIX 2', LAUNCH_TIME_DICT)
  drawByModel('MI 5', LAUNCH_TIME_DICT)
  drawByModel('MI 4 LTE', LAUNCH_TIME_DICT)
  drawByModel('MI NOTE LTE', LAUNCH_TIME_DICT)
  drawByModel('Redmi Note 4X', LAUNCH_TIME_DICT)  


def main():
  parseFile()
  # draw()
  




if __name__ == '__main__':
  print 'len(sys.argv)', len(sys.argv) 
  print '---------- sys.argv', sys.argv
  FILE_NAME = sys.argv[1]
  main()
